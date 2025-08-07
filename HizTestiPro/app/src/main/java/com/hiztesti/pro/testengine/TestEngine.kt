package com.hiztesti.pro.testengine

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlin.math.abs

sealed class SegmentType { object Accelerate : SegmentType(); object Brake : SegmentType() }

data class SpeedSegment(val type: SegmentType, val fromKmh: Double, val toKmh: Double)

data class SegmentResult(
    val segment: SpeedSegment,
    val durationSeconds: Double,
    val distanceMeters: Double
)

data class TestResult(
    val results: List<SegmentResult>,
    val totalTimeSeconds: Double,
    val totalDistanceMeters: Double
)

class TestEngine(private val segments: List<SpeedSegment>) {
    data class Live(
        val currentSpeedKmh: Double = 0.0,
        val distanceMeters: Double = 0.0,
        val elapsedSeconds: Double = 0.0,
        val activeIndex: Int = 0
    )

    private val _live = MutableStateFlow(Live())
    val live: StateFlow<Live> = _live

    private var isRunning = false
    private var currentIndex = 0
    private var lastTimestampMs: Long? = null
    private var accumulatedDistance = 0.0
    private var accumulatedTime = 0.0

    private val results = mutableListOf<SegmentResult>()
    private var segmentStartTime = 0.0
    private var segmentStartDistance = 0.0

    fun start() {
        isRunning = true
        currentIndex = 0
        results.clear()
        accumulatedDistance = 0.0
        accumulatedTime = 0.0
        segmentStartTime = 0.0
        segmentStartDistance = 0.0
        lastTimestampMs = null
        _live.value = Live()
    }

    fun stop(): TestResult? {
        if (!isRunning) return null
        isRunning = false
        val total = TestResult(results.toList(), accumulatedTime, accumulatedDistance)
        return total
    }

    fun onTick(speedKmh: Double, timestampMs: Long) {
        if (!isRunning) return
        val dt = lastTimestampMs?.let { (timestampMs - it).coerceAtLeast(0) / 1000.0 } ?: 0.0
        lastTimestampMs = timestampMs
        if (dt <= 0.0 || dt > 1.0) return

        // integrate distance (v[m/s] * dt)
        val distanceDelta = (speedKmh / 3.6) * dt
        accumulatedDistance += distanceDelta
        accumulatedTime += dt

        val seg = segments.getOrNull(currentIndex) ?: run { stop(); return }
        val progress = checkSegmentProgress(seg, speedKmh)
        if (progress) {
            val segmentTime = accumulatedTime - segmentStartTime
            val segmentDistance = accumulatedDistance - segmentStartDistance
            results.add(SegmentResult(seg, segmentTime, segmentDistance))
            currentIndex += 1
            if (currentIndex >= segments.size) {
                stop()
            } else {
                segmentStartTime = accumulatedTime
                segmentStartDistance = accumulatedDistance
            }
        }

        _live.value = _live.value.copy(
            currentSpeedKmh = speedKmh,
            distanceMeters = accumulatedDistance,
            elapsedSeconds = accumulatedTime,
            activeIndex = currentIndex
        )
    }

    private fun checkSegmentProgress(segment: SpeedSegment, speedKmh: Double): Boolean {
        return when (segment.type) {
            is SegmentType.Accelerate -> speedKmh >= segment.toKmh - 0.5 && speedKmh >= segment.fromKmh - 0.5
            is SegmentType.Brake -> speedKmh <= segment.toKmh + 0.5 && speedKmh <= segment.fromKmh + 5.0
        }
    }
}