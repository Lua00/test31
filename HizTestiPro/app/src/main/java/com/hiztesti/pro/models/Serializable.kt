package com.hiztesti.pro.models

import kotlinx.serialization.Serializable

@Serializable
data class SavedSegment(
    val type: String,
    val fromKmh: Double,
    val toKmh: Double,
    val durationSeconds: Double,
    val distanceMeters: Double
)

@Serializable
data class SavedResult(
    val testName: String,
    val startedAtEpochMs: Long,
    val totalTimeSeconds: Double,
    val totalDistanceMeters: Double,
    val segments: List<SavedSegment>
)