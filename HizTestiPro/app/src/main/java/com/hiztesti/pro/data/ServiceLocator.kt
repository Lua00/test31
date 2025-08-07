package com.hiztesti.pro.data

import android.content.Context
import androidx.room.Room
import com.hiztesti.pro.data.db.AppDatabase
import com.hiztesti.pro.location.GnssRepository
import com.hiztesti.pro.location.LocationRepository
import com.hiztesti.pro.sensors.SensorRepository

object ServiceLocator {
    @Volatile private var databaseInstance: AppDatabase? = null
    @Volatile private var locationRepositoryInstance: LocationRepository? = null
    @Volatile private var sensorRepositoryInstance: SensorRepository? = null
    @Volatile private var gnssRepositoryInstance: GnssRepository? = null
    @Volatile private var preferencesRepositoryInstance: PreferencesRepository? = null

    fun db(context: Context): AppDatabase = databaseInstance ?: synchronized(this) {
        databaseInstance ?: Room.databaseBuilder(
            context.applicationContext,
            AppDatabase::class.java,
            "hiz_testi.db"
        ).fallbackToDestructiveMigration().build().also { databaseInstance = it }
    }

    fun sessionDao(context: Context) = db(context).sessionDao()

    fun locationRepository(context: Context): LocationRepository =
        locationRepositoryInstance ?: synchronized(this) {
            locationRepositoryInstance ?: LocationRepository(context.applicationContext).also { locationRepositoryInstance = it }
        }

    fun gnssRepository(context: Context): GnssRepository =
        gnssRepositoryInstance ?: synchronized(this) {
            gnssRepositoryInstance ?: GnssRepository(context.applicationContext).also { gnssRepositoryInstance = it }
        }

    fun sensorRepository(context: Context): SensorRepository =
        sensorRepositoryInstance ?: synchronized(this) {
            sensorRepositoryInstance ?: SensorRepository(context.applicationContext).also { sensorRepositoryInstance = it }
        }

    fun preferences(context: Context): PreferencesRepository =
        preferencesRepositoryInstance ?: synchronized(this) {
            preferencesRepositoryInstance ?: PreferencesRepository(context.applicationContext).also { preferencesRepositoryInstance = it }
        }
}