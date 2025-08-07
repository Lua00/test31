package com.hiztesti.pro.estimation

import android.location.Location
import kotlin.math.max
import kotlin.math.min

class SpeedEstimator(
    private val gpsTrust: Double = 0.85,
    private val accelTrust: Double = 0.15
) {
    private var lastTimestampMs: Long? = null
    private var estimatedSpeedMps: Double = 0.0

    fun onGps(location: Location) {
        val gpsSpeed = if (location.hasSpeed()) location.speed.toDouble() else null
        if (gpsSpeed != null) {
            estimatedSpeedMps = gpsTrust * gpsSpeed + (1 - gpsTrust) * estimatedSpeedMps
        }
    }

    fun onLinearAcceleration(ax: Float, ay: Float, az: Float, timestampMs: Long) {
        val dt = lastTimestampMs?.let { (timestampMs - it).coerceAtLeast(0) / 1000.0 } ?: 0.0
        lastTimestampMs = timestampMs
        if (dt <= 0.0 || dt > 1.0) return
        val forwardAccel = ax.toDouble() // naive; ideally rotate into vehicle frame
        val integrated = estimatedSpeedMps + forwardAccel * dt
        estimatedSpeedMps = accelTrust * integrated + (1 - accelTrust) * estimatedSpeedMps
        estimatedSpeedMps = max(0.0, estimatedSpeedMps)
    }

    fun getSpeedMps(): Double = estimatedSpeedMps
    fun getSpeedKmh(): Double = estimatedSpeedMps * 3.6
}