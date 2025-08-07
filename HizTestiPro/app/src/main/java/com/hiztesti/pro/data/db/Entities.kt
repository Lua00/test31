package com.hiztesti.pro.data.db

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "test_session")
data class TestSessionEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val startedAtEpochMs: Long,
    val totalTimeSeconds: Double,
    val totalDistanceMeters: Double,
    val segmentsJson: String,
    val testName: String
)