package com.hiztesti.pro.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.hiztesti.pro.data.ServiceLocator
import com.hiztesti.pro.data.db.VehicleEntity
import kotlinx.coroutines.launch

class AddVehicleViewModel(app: Application) : AndroidViewModel(app) {
    private val dao = ServiceLocator.db(app).vehicleDao()

    fun save(plate: String, km: Long, model: String?) {
        viewModelScope.launch {
            dao.insert(VehicleEntity(plate = plate, km = km, model = model))
        }
    }
}