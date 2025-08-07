package com.hiztesti.pro.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.hiztesti.pro.data.ServiceLocator
import com.hiztesti.pro.data.db.TestSessionEntity
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class HistoryViewModel(app: Application) : AndroidViewModel(app) {
    private val sessionDao = ServiceLocator.sessionDao(app)

    private val _items = MutableStateFlow<List<TestSessionEntity>>(emptyList())
    val items: StateFlow<List<TestSessionEntity>> = _items

    fun load() {
        viewModelScope.launch {
            _items.value = sessionDao.all()
        }
    }
}