package com.hiztesti.pro.ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.hiztesti.pro.viewmodel.SettingsViewModel

@Composable
fun SettingsScreen(navController: NavController, vm: SettingsViewModel = viewModel()) {
    val unit by vm.unit.collectAsState()
    val gpsMs by vm.gpsIntervalMs.collectAsState()
    val unitText = remember { mutableStateOf(unit) }
    val gpsText = remember { mutableStateOf(gpsMs.toString()) }

    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text("Ayarlar")
        OutlinedTextField(value = unitText.value, onValueChange = { unitText.value = it }, label = { Text("Birim (kmh/mph)") })
        OutlinedTextField(value = gpsText.value, onValueChange = { gpsText.value = it }, label = { Text("GPS aralık (ms)") })
        Button(onClick = {
            vm.setUnit(unitText.value)
            vm.setGpsInterval(gpsText.value.toIntOrNull() ?: 200)
        }, modifier = Modifier.padding(top = 12.dp)) { Text("Kaydet") }
    }
}