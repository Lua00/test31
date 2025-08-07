package com.hiztesti.pro.data

import android.content.Context
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.doublePreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore by preferencesDataStore("settings")

class PreferencesRepository(private val context: Context) {
    object Keys {
        val unit = stringPreferencesKey("unit") // "kmh" or "mph"
        val gpsIntervalMs = intPreferencesKey("gpsIntervalMs")
        val sensorDelay = intPreferencesKey("sensorDelay") // SensorManager delays
        val soundCues = booleanPreferencesKey("soundCues")
        val smoothing = doublePreferencesKey("smoothing")
    }

    val unitFlow: Flow<String> = context.dataStore.data.map { it[Keys.unit] ?: "kmh" }
    val gpsIntervalFlow: Flow<Int> = context.dataStore.data.map { it[Keys.gpsIntervalMs] ?: 200 }
    val sensorDelayFlow: Flow<Int> = context.dataStore.data.map { it[Keys.sensorDelay] ?: 2 }
    val soundCuesFlow: Flow<Boolean> = context.dataStore.data.map { it[Keys.soundCues] ?: false }
    val smoothingFlow: Flow<Double> = context.dataStore.data.map { it[Keys.smoothing] ?: 0.15 }

    suspend fun setUnit(value: String) { context.dataStore.edit { it[Keys.unit] = value } }
    suspend fun setGpsInterval(ms: Int) { context.dataStore.edit { it[Keys.gpsIntervalMs] = ms } }
    suspend fun setSensorDelay(delay: Int) { context.dataStore.edit { it[Keys.sensorDelay] = delay } }
    suspend fun setSoundCues(on: Boolean) { context.dataStore.edit { it[Keys.soundCues] = on } }
    suspend fun setSmoothing(value: Double) { context.dataStore.edit { it[Keys.smoothing] = value } }
}