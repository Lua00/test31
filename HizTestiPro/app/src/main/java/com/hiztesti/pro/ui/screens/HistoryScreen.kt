package com.hiztesti.pro.ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.hiztesti.pro.data.db.TestSessionEntity
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import com.hiztesti.pro.models.SavedSegment
import androidx.compose.ui.unit.dp

@Composable
fun HistoryScreen(navController: NavController, vm: com.hiztesti.pro.viewmodel.HistoryViewModel = viewModel()) {
    val items by vm.items.collectAsState()
    LaunchedEffect(Unit) { vm.load() }

    Column(modifier = Modifier.fillMaxSize()) {
        Text("Geçmiş Kayıtlar")
        LazyColumn {
            items(items) { entity ->
                HistoryItem(entity)
            }
        }
    }
}

@Composable
private fun HistoryItem(entity: TestSessionEntity) {
    val segments: List<SavedSegment> = try {
        Json.decodeFromString(entity.segmentsJson)
    } catch (e: Exception) { emptyList() }
    Card { 
        Column(modifier = androidx.compose.ui.Modifier.fillMaxSize().padding(12.dp)) {
            Text(entity.testName)
            Text("Toplam süre: ${"% .3f".format(entity.totalTimeSeconds)} s")
            Text("Toplam mesafe: ${"% .2f".format(entity.totalDistanceMeters)} m")
            segments.take(3).forEachIndexed { index, s ->
                Text("${index+1}. ${s.type} ${s.fromKmh}-${s.toKmh} km/h: ${"% .3f".format(s.durationSeconds)} s, ${"% .2f".format(s.distanceMeters)} m")
            }
        }
    }
}