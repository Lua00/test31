package com.hiztesti.pro.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Home
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
import com.hiztesti.pro.ui.screens.DashboardScreen
import com.hiztesti.pro.ui.screens.HistoryScreen
import com.hiztesti.pro.ui.screens.SettingsScreen
import com.hiztesti.pro.ui.screens.TestScreen
import androidx.compose.foundation.layout.padding

sealed class Route(val route: String, val label: String) {
    data object Dashboard : Route("dashboard", "Ana Sayfa")
    data object Test : Route("test", "Test")
    data object History : Route("history", "Geçmiş")
    data object Settings : Route("settings", "Ayarlar")
}

@Composable
fun AppNav() {
    val navController = rememberNavController()
    val items = listOf(Route.Dashboard, Route.Test, Route.History, Route.Settings)
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
                                popUpTo(Route.Dashboard.route)
                                launchSingleTop = true
                            }
                        },
                        icon = {
                            when (item) {
                                Route.Dashboard -> Icon(Icons.Default.Home, contentDescription = null)
                                Route.History -> Icon(Icons.Default.History, contentDescription = null)
                                Route.Settings -> Icon(Icons.Default.Settings, contentDescription = null)
                                else -> Icon(Icons.Default.Home, contentDescription = null)
                            }
                        },
                        label = { Text(item.label) }
                    )
                }
            }
        }
    ) { padding ->
        androidx.compose.foundation.layout.Box(modifier = androidx.compose.ui.Modifier.padding(padding)) {
            NavHost(navController = navController, startDestination = Route.Dashboard.route) {
                composable(Route.Dashboard.route) { DashboardScreen(navController) }
                composable(Route.Test.route) { TestScreen(navController) }
                composable(Route.History.route) { HistoryScreen(navController) }
                composable(Route.Settings.route) { SettingsScreen(navController) }
            }
        }
    }
}