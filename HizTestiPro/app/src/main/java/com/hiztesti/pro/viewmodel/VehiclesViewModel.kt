package com.hiztesti.pro.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.hiztesti.pro.data.ServiceLocator
import com.hiztesti.pro.data.db.VehicleEntity
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class VehiclesViewModel(app: Application) : AndroidViewModel(app) {
    private val dao = ServiceLocator.db(app).vehicleDao()
    private val _items = MutableStateFlow<List<VehicleEntity>>(emptyList())
    val items: StateFlow<List<VehicleEntity>> = _items

    fun load() { viewModelScope.launch { _items.value = dao.all() } }
}