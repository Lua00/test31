package com.hiztesti.pro.navigation

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.hiztesti.pro.ui.screens.DashboardScreen
import com.hiztesti.pro.ui.screens.HistoryScreen
import com.hiztesti.pro.ui.screens.TestScreen

sealed class Route(val route: String) {
    data object Dashboard : Route("dashboard")
    data object Test : Route("test")
    data object History : Route("history")
}

@Composable
fun AppNav() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = Route.Dashboard.route) {
        composable(Route.Dashboard.route) { DashboardScreen(navController) }
        composable(Route.Test.route) { TestScreen(navController) }
        composable(Route.History.route) { HistoryScreen(navController) }
    }
}