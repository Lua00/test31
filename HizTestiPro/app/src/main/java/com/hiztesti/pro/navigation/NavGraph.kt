package com.hiztesti.pro.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.DirectionsCar
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.hiztesti.pro.ui.screens.AddVehicleScreen
import com.hiztesti.pro.ui.screens.SettingsScreen
import com.hiztesti.pro.ui.screens.VehicleDetailScreen
import com.hiztesti.pro.ui.screens.VehiclesScreen
import androidx.compose.foundation.layout.padding

sealed class Route(val route: String, val label: String) {
    data object Vehicles : Route("vehicles", "Araçlar")
    data object AddVehicle : Route("add_vehicle", "Ekle")
    data object VehicleDetail : Route("vehicle_detail", "Detay")
    data object Settings : Route("settings", "Ayarlar")
}

@Composable
fun AppNav() {
    val navController = rememberNavController()
    val items = listOf(Route.Vehicles, Route.AddVehicle, Route.Settings)
    Scaffold(
        bottomBar = {
            NavigationBar {
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentRoute = navBackStackEntry?.destination?.route
                items.forEach { item ->
                    NavigationBarItem(
                        selected = currentRoute == item.route,
                        onClick = {
                            if (currentRoute != item.route) navController.navigate(item.route) {
                                popUpTo(Route.Vehicles.route)
                                launchSingleTop = true
                            }
                        },
                        icon = {
                            when (item) {
                                Route.Vehicles -> Icon(Icons.Default.DirectionsCar, contentDescription = null)
                                Route.AddVehicle -> Icon(Icons.Default.Add, contentDescription = null)
                                Route.Settings -> Icon(Icons.Default.Settings, contentDescription = null)
                                else -> Icon(Icons.Default.DirectionsCar, contentDescription = null)
                            }
                        },
                        label = { Text(item.label) }
                    )
                }
            }
        }
    ) { padding ->
        androidx.compose.foundation.layout.Box(modifier = androidx.compose.ui.Modifier.padding(padding)) {
            NavHost(navController = navController, startDestination = Route.Vehicles.route) {
                composable(Route.Vehicles.route) { VehiclesScreen(navController) }
                composable(Route.AddVehicle.route) { AddVehicleScreen(navController) }
                composable(Route.VehicleDetail.route) { VehicleDetailScreen(navController) }
                composable(Route.Settings.route) { SettingsScreen(navController) }
            }
        }
    }
}