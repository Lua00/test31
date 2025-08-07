package com.hiztesti.pro.viewmodel

import android.app.Application
import android.content.Intent
import android.location.Location
import androidx.core.content.ContextCompat
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.hiztesti.pro.data.ServiceLocator
import com.hiztesti.pro.data.db.TestSessionEntity
import com.hiztesti.pro.estimation.SpeedEstimator
import com.hiztesti.pro.models.SavedResult
import com.hiztesti.pro.models.SavedSegment
import com.hiztesti.pro.service.TelemetryService
import com.hiztesti.pro.testengine.SegmentType
import com.hiztesti.pro.testengine.SpeedSegment
import com.hiztesti.pro.testengine.TestEngine
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

class TelemetryViewModel(app: Application) : AndroidViewModel(app) {

    data class TelemetryState(
        val speedKmh: Double = 0.0,
        val gForce: Double = 0.0,
        val distanceMeters: Double = 0.0,
        val elapsedSeconds: Double = 0.0,
        val isRunning: Boolean = false,
        val activeSegmentIndex: Int = 0,
        val testName: String = "",
        val satellitesUsed: Int = 0,
        val satellitesTotal: Int = 0
    )

    private val locationRepo = ServiceLocator.locationRepository(app)
    private val gnssRepo = ServiceLocator.gnssRepository(app)
    private val sensorRepo = ServiceLocator.sensorRepository(app)
    private val sessionDao = ServiceLocator.sessionDao(app)

    private val estimator = SpeedEstimator()
    private var engine: TestEngine? = null
    private var collector: Job? = null

    private val _state = MutableStateFlow(TelemetryState())
    val state: StateFlow<TelemetryState> = _state

    fun startTest(testName: String, segments: List<SpeedSegment>) {
        engine = TestEngine(segments).also { it.start() }
        _state.value = _state.value.copy(isRunning = true, testName = testName)
        startService()
        collector?.cancel()
        collector = viewModelScope.launch(Dispatchers.Default) {
            val locations = locationRepo.locationUpdates().onEach { onGps(it) }
            val linAcc = sensorRepo.linearAcceleration()
            val sats = gnssRepo.satelliteCounts()
            combine(linAcc, locations, sats) { accValues, _, satPair -> Triple(accValues, Unit, satPair) }
                .collect { (accValues, _, satPair) ->
                    val now = System.currentTimeMillis()
                    val ax = accValues.getOrNull(0) ?: 0f
                    val ay = accValues.getOrNull(1) ?: 0f
                    val az = accValues.getOrNull(2) ?: 0f
                    estimator.onLinearAcceleration(ax, ay, az, now)
                    val speedKmh = estimator.getSpeedKmh()
                    engine?.onTick(speedKmh, now)
                    val live = engine?.live?.value
                    val gForce = ax.toDouble() / 9.80665
                    val satellitesUsed = satPair.first
                    val satellitesTotal = satPair.second
                    val newState = _state.value.copy(
                        speedKmh = speedKmh,
                        gForce = gForce,
                        distanceMeters = live?.distanceMeters ?: 0.0,
                        elapsedSeconds = live?.elapsedSeconds ?: 0.0,
                        activeSegmentIndex = live?.activeIndex ?: 0,
                        satellitesUsed = satellitesUsed,
                        satellitesTotal = satellitesTotal
                    )
                    _state.value = newState
                }
        }
    }

    private fun onGps(location: Location) {
        estimator.onGps(location)
    }

    fun stopTest() {
        val result = engine?.stop()
        collector?.cancel()
        _state.value = _state.value.copy(isRunning = false)
        stopService()
        result ?: return
        viewModelScope.launch(Dispatchers.IO) {
            val saved = SavedResult(
                testName = _state.value.testName,
                startedAtEpochMs = System.currentTimeMillis(),
                totalTimeSeconds = result.totalTimeSeconds,
                totalDistanceMeters = result.totalDistanceMeters,
                segments = result.results.map {
                    SavedSegment(
                        type = when (it.segment.type) {
                            is SegmentType.Accelerate -> "accelerate"
                            is SegmentType.Brake -> "brake"
                        },
                        fromKmh = it.segment.fromKmh,
                        toKmh = it.segment.toKmh,
                        durationSeconds = it.durationSeconds,
                        distanceMeters = it.distanceMeters
                    )
                }
            )
            val json = Json.encodeToString(saved.segments)
            sessionDao.insert(
                TestSessionEntity(
                    startedAtEpochMs = saved.startedAtEpochMs,
                    totalTimeSeconds = saved.totalTimeSeconds,
                    totalDistanceMeters = saved.totalDistanceMeters,
                    segmentsJson = json,
                    testName = saved.testName
                )
            )
        }
    }

    private fun startService() {
        try {
            val ctx = getApplication<Application>()
            val intent = Intent(ctx, TelemetryService::class.java)
            ContextCompat.startForegroundService(ctx, intent)
        } catch (_: Exception) { }
    }

    private fun stopService() {
        try {
            val ctx = getApplication<Application>()
            val intent = Intent(ctx, TelemetryService::class.java)
            ctx.stopService(intent)
        } catch (_: Exception) { }
    }

    fun predefinedTests(): List<Pair<String, List<SpeedSegment>>> = listOf(
        "0-100-0" to listOf(
            SpeedSegment(SegmentType.Accelerate, 0.0, 100.0),
            SpeedSegment(SegmentType.Brake, 100.0, 0.0)
        ),
        "0-50" to listOf(
            SpeedSegment(SegmentType.Accelerate, 0.0, 50.0)
        ),
        "50-60-100-0" to listOf(
            SpeedSegment(SegmentType.Accelerate, 50.0, 60.0),
            SpeedSegment(SegmentType.Accelerate, 60.0, 100.0),
            SpeedSegment(SegmentType.Brake, 100.0, 0.0)
        ),
        "0-200-0" to listOf(
            SpeedSegment(SegmentType.Accelerate, 0.0, 200.0),
            SpeedSegment(SegmentType.Brake, 200.0, 0.0)
        )
    )
}