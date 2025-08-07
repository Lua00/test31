package com.hiztesti.pro.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.hiztesti.pro.navigation.Route

@Composable
fun DashboardScreen(navController: NavController) {
    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Hız Testi Pro", style = MaterialTheme.typography.headlineLarge)
        Text("0-100-0, 0-50, 50-60-100-0 hızlanma/fren testleri", style = MaterialTheme.typography.bodyMedium)

        Button(onClick = { navController.navigate(Route.Test.route) }, modifier = Modifier.padding(top = 24.dp)) {
            Text("Testi Başlat")
        }

        Button(onClick = { navController.navigate(Route.History.route) }, modifier = Modifier.padding(top = 12.dp)) {
            Text("Geçmiş")
        }
    }
}