package com.hiztesti.pro.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.hiztesti.pro.navigation.Route
import com.hiztesti.pro.viewmodel.VehiclesViewModel

@Composable
fun VehiclesScreen(navController: NavController, vm: VehiclesViewModel = viewModel()) {
    val vehicles by vm.items.collectAsState()
    LaunchedEffect(Unit) { vm.load() }

    Column(modifier = Modifier.fillMaxSize()) {
        Text("Araçlar", style = MaterialTheme.typography.headlineMedium)
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(vehicles) { v ->
                Card(modifier = Modifier.clickable { navController.navigate(Route.VehicleDetail.route) }) {
                    Column(modifier = Modifier) {
                        Text(v.plate)
                        Text("KM: ${v.km}")
                        Text(v.model ?: "")
                    }
                }
            }
        }
    }
    FloatingActionButton(onClick = { navController.navigate(Route.AddVehicle.route) }) {
        Icon(Icons.Filled.Add, contentDescription = null)
    }
}