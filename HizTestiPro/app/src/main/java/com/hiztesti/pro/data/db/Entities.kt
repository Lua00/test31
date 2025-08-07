package com.hiztesti.pro.data.db

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "vehicle")
data class VehicleEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val plate: String,
    val km: Long,
    val model: String? = null
)

@Entity(tableName = "vehicle_log")
data class VehicleLogEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val vehicleId: Long,
    val type: String, // maintenance or repair
    val title: String,
    val note: String? = null,
    val photoPath: String? = null,
    val createdAt: Long
)