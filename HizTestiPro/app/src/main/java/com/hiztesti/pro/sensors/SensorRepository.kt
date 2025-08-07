package com.hiztesti.pro.sensors

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow

class SensorRepository(context: Context) {
    private val sensorManager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager

    fun linearAcceleration(): Flow<FloatArray> = sensorFlow(Sensor.TYPE_LINEAR_ACCELERATION, SensorManager.SENSOR_DELAY_GAME)
    fun gyroscope(): Flow<FloatArray> = sensorFlow(Sensor.TYPE_GYROSCOPE, SensorManager.SENSOR_DELAY_GAME)

    private fun sensorFlow(sensorType: Int, delay: Int): Flow<FloatArray> = callbackFlow {
        val sensor = sensorManager.getDefaultSensor(sensorType)
        val listener = object : SensorEventListener {
            override fun onSensorChanged(event: SensorEvent) {
                trySend(event.values.clone())
            }
            override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}
        }
        sensor?.let { sensorManager.registerListener(listener, it, delay) }
        awaitClose { sensorManager.unregisterListener(listener) }
    }
}