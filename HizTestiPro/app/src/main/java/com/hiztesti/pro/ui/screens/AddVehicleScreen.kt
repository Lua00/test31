package com.hiztesti.pro.ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.hiztesti.pro.viewmodel.AddVehicleViewModel

@Composable
fun AddVehicleScreen(navController: NavController, vm: AddVehicleViewModel = viewModel()) {
    val plate = remember { mutableStateOf("") }
    val km = remember { mutableStateOf("") }
    val model = remember { mutableStateOf("") }
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text("Araç Ekle")
        OutlinedTextField(plate.value, { plate.value = it }, label = { Text("Plaka") })
        OutlinedTextField(km.value, { km.value = it }, label = { Text("KM") })
        OutlinedTextField(model.value, { model.value = it }, label = { Text("Model") })
        Button(onClick = {
            vm.save(plate.value, km.value.toLongOrNull() ?: 0L, model.value)
            navController.popBackStack()
        }, modifier = Modifier.padding(top = 12.dp)) { Text("Kaydet") }
    }
}