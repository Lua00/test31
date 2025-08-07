package com.hiztesti.pro.data.db

import androidx.room.Dao
import androidx.room.Database
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.RoomDatabase

@Database(entities = [VehicleEntity::class, VehicleLogEntity::class], version = 1, exportSchema = true)
abstract class AppDatabase : RoomDatabase() {
    abstract fun vehicleDao(): VehicleDao
    abstract fun vehicleLogDao(): VehicleLogDao
}

@Dao
interface VehicleDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: VehicleEntity): Long

    @Query("SELECT * FROM vehicle ORDER BY id DESC")
    suspend fun all(): List<VehicleEntity>
}

@Dao
interface VehicleLogDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: VehicleLogEntity): Long

    @Query("SELECT * FROM vehicle_log WHERE vehicleId = :vehicleId ORDER BY createdAt DESC")
    suspend fun logsFor(vehicleId: Long): List<VehicleLogEntity>
}