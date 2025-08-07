package com.hiztesti.pro.data.db

import androidx.room.Dao
import androidx.room.Database
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.RoomDatabase

@Database(entities = [TestSessionEntity::class], version = 1, exportSchema = true)
abstract class AppDatabase : RoomDatabase() {
    abstract fun sessionDao(): SessionDao
}

@Dao
interface SessionDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: TestSessionEntity): Long

    @Query("SELECT * FROM test_session ORDER BY startedAtEpochMs DESC")
    suspend fun all(): List<TestSessionEntity>
}