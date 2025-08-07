package com.hiztesti.pro.data

import android.content.Context
import androidx.room.Room
import com.hiztesti.pro.data.db.AppDatabase

object ServiceLocator {
    @Volatile private var databaseInstance: AppDatabase? = null
    @Volatile private var preferencesRepositoryInstance: PreferencesRepository? = null

    fun db(context: Context): AppDatabase = databaseInstance ?: synchronized(this) {
        databaseInstance ?: Room.databaseBuilder(
            context.applicationContext,
            AppDatabase::class.java,
            "arcar.db"
        ).fallbackToDestructiveMigration().build().also { databaseInstance = it }
    }

    fun preferences(context: Context): PreferencesRepository =
        preferencesRepositoryInstance ?: synchronized(this) {
            preferencesRepositoryInstance ?: PreferencesRepository(context.applicationContext).also { preferencesRepositoryInstance = it }
        }
}