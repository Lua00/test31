package com.hiztesti.pro.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.hiztesti.pro.testengine.SpeedSegment
import com.hiztesti.pro.viewmodel.TelemetryViewModel

@Composable
fun TestScreen(navController: NavController, vm: TelemetryViewModel = viewModel()) {
    val state by vm.state.collectAsState()
    val presets = remember { vm.predefinedTests() }
    val selected = remember { mutableIntStateOf(0) }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp).verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.Top,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Canlı Telemetri", style = MaterialTheme.typography.headlineMedium)
        Spacer(Modifier.height(12.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            presets.forEachIndexed { index, pair ->
                FilterChip(
                    selected = selected.intValue == index,
                    onClick = { selected.intValue = index },
                    label = { Text(pair.first) }
                )
            }
        }
        Spacer(Modifier.height(16.dp))
        Card(modifier = Modifier.padding(8.dp)) {
            Column(Modifier.padding(16.dp)) {
                Text("Hız: ${"%,.1f".format(state.speedKmh)} km/h", style = MaterialTheme.typography.headlineSmall)
                Text("G Kuvveti: ${"% .2f".format(state.gForce)} g")
                Text("Mesafe: ${"% .2f".format(state.distanceMeters)} m")
                Text("Süre: ${"% .3f".format(state.elapsedSeconds)} s")
                Text("Aşama: ${state.activeSegmentIndex + 1}")
            }
        }
        Spacer(Modifier.height(16.dp))
        Button(onClick = {
            if (state.isRunning) vm.stopTest() else {
                val (name, segs) = presets[selected.intValue]
                vm.startTest(name, segs)
            }
        }) {
            Text(if (state.isRunning) "Testi Bitir" else "Testi Başlat")
        }
    }
}