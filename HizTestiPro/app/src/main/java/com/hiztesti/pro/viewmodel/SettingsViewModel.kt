package com.hiztesti.pro.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.hiztesti.pro.data.ServiceLocator
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class SettingsViewModel(app: Application) : AndroidViewModel(app) {
    private val prefs = ServiceLocator.preferences(app)

    val unit: StateFlow<String> = prefs.unitFlow.stateIn(viewModelScope, SharingStarted.Eagerly, "kmh")
    val gpsIntervalMs: StateFlow<Int> = prefs.gpsIntervalFlow.stateIn(viewModelScope, SharingStarted.Eagerly, 200)

    fun setUnit(value: String) { viewModelScope.launch { prefs.setUnit(value.lowercase()) } }
    fun setGpsInterval(ms: Int) { viewModelScope.launch { prefs.setGpsInterval(ms) } }
}