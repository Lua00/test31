import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  StatusBar,
  RefreshControl,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import LinearGradient from 'react-native-linear-gradient';

import { Vehicle, MaintenanceRecord } from '../types';
import { StorageService } from '../services/StorageService';
import VehicleCard from '../components/VehicleCard';
import MaintenanceCard from '../components/MaintenanceCard';

const HomeScreen: React.FC = () => {
  const navigation = useNavigation();
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [recentMaintenance, setRecentMaintenance] = useState<MaintenanceRecord[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [vehiclesData, maintenanceData] = await Promise.all([
        StorageService.getVehicles(),
        StorageService.getMaintenanceRecords(),
      ]);
      
      setVehicles(vehiclesData);
      
      // Get last 3 maintenance records
      const sortedMaintenance = maintenanceData
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
        .slice(0, 3);
      setRecentMaintenance(sortedMaintenance);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  const getVehicleById = (vehicleId: string) => {
    return vehicles.find(v => v.id === vehicleId);
  };

  return (
    <View style={styles.container}>
      <StatusBar backgroundColor="#2563eb" barStyle="light-content" />
      
      <LinearGradient
        colors={['#3b82f6', '#2563eb']}
        style={styles.header}>
        <View style={styles.headerContent}>
          <Text style={styles.headerTitle}>Arcar</Text>
          <Text style={styles.headerSubtitle}>Araç Bakım Günlüğü</Text>
        </View>
      </LinearGradient>

      <ScrollView
        style={styles.content}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }>
        
        {/* Statistics */}
        <View style={styles.statsContainer}>
          <View style={styles.statCard}>
            <Icon name="directions-car" size={24} color="#3b82f6" />
            <Text style={styles.statNumber}>{vehicles.length}</Text>
            <Text style={styles.statLabel}>Araç</Text>
          </View>
          
          <View style={styles.statCard}>
            <Icon name="build" size={24} color="#10b981" />
            <Text style={styles.statNumber}>{recentMaintenance.length}</Text>
            <Text style={styles.statLabel}>Son Bakım</Text>
          </View>
        </View>

        {/* Recent Vehicles */}
        {vehicles.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Araçlarım</Text>
            {vehicles.slice(0, 2).map((vehicle) => (
              <VehicleCard
                key={vehicle.id}
                vehicle={vehicle}
                onPress={() => navigation.navigate('VehicleDetail', { vehicleId: vehicle.id })}
              />
            ))}
            {vehicles.length > 2 && (
              <Text 
                style={styles.viewAllText}
                onPress={() => navigation.navigate('VehicleStack')}>
                Tümünü Gör ({vehicles.length - 2} daha)
              </Text>
            )}
          </View>
        )}

        {/* Recent Maintenance */}
        {recentMaintenance.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Son Bakım/Tamir İşlemleri</Text>
            {recentMaintenance.map((record) => {
              const vehicle = getVehicleById(record.vehicleId);
              return (
                <View key={record.id} style={styles.maintenanceItem}>
                  {vehicle && (
                    <Text style={styles.vehicleLabel}>
                      {vehicle.brand} {vehicle.model} - {vehicle.licensePlate}
                    </Text>
                  )}
                  <MaintenanceCard
                    record={record}
                    onPress={() => navigation.navigate('MaintenanceDetail', { maintenanceId: record.id })}
                  />
                </View>
              );
            })}
          </View>
        )}

        {/* Empty State */}
        {vehicles.length === 0 && (
          <View style={styles.emptyState}>
            <Icon name="directions-car" size={64} color="#9ca3af" />
            <Text style={styles.emptyTitle}>Henüz araç eklemediniz</Text>
            <Text style={styles.emptyDescription}>
              İlk aracınızı ekleyerek bakım takibine başlayın
            </Text>
          </View>
        )}

        <View style={styles.bottomPadding} />
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  header: {
    paddingTop: 48,
    paddingBottom: 24,
    paddingHorizontal: 20,
  },
  headerContent: {
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#dbeafe',
  },
  content: {
    flex: 1,
  },
  statsContainer: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingVertical: 20,
    gap: 16,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.05,
    shadowRadius: 4,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1f2937',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 4,
  },
  section: {
    marginTop: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 16,
    paddingHorizontal: 16,
  },
  viewAllText: {
    textAlign: 'center',
    color: '#3b82f6',
    fontSize: 14,
    fontWeight: '500',
    marginTop: 16,
    paddingHorizontal: 16,
  },
  maintenanceItem: {
    marginBottom: 8,
  },
  vehicleLabel: {
    fontSize: 12,
    color: '#6b7280',
    fontWeight: '500',
    marginLeft: 16,
    marginBottom: 4,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 64,
    paddingHorizontal: 32,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#4b5563',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyDescription: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 20,
  },
  bottomPadding: {
    height: 24,
  },
});

export default HomeScreen;