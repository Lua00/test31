import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  StyleSheet,
  FlatList,
  Alert,
  RefreshControl,
} from 'react-native';
import { useNavigation, useFocusEffect } from '@react-navigation/native';

import { Vehicle } from '../types';
import { StorageService } from '../services/StorageService';
import VehicleCard from '../components/VehicleCard';
import FloatingActionButton from '../components/FloatingActionButton';

const VehicleListScreen: React.FC = () => {
  const navigation = useNavigation();
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  useFocusEffect(
    useCallback(() => {
      loadVehicles();
    }, [])
  );

  const loadVehicles = async () => {
    try {
      const vehiclesData = await StorageService.getVehicles();
      setVehicles(vehiclesData);
    } catch (error) {
      console.error('Error loading vehicles:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadVehicles();
    setRefreshing(false);
  };

  const handleVehiclePress = (vehicleId: string) => {
    navigation.navigate('VehicleDetail', { vehicleId });
  };

  const handleEditVehicle = (vehicleId: string) => {
    navigation.navigate('EditVehicle', { vehicleId });
  };

  const handleDeleteVehicle = (vehicle: Vehicle) => {
    Alert.alert(
      'Araç Sil',
      `${vehicle.brand} ${vehicle.model} aracını silmek istediğinizden emin misiniz? Bu işlem geri alınamaz ve tüm bakım kayıtları da silinecektir.`,
      [
        {
          text: 'İptal',
          style: 'cancel',
        },
        {
          text: 'Sil',
          style: 'destructive',
          onPress: async () => {
            try {
              await StorageService.deleteVehicle(vehicle.id);
              await loadVehicles();
            } catch (error) {
              console.error('Error deleting vehicle:', error);
              Alert.alert('Hata', 'Araç silinirken bir hata oluştu.');
            }
          },
        },
      ]
    );
  };

  const handleAddVehicle = () => {
    navigation.navigate('AddVehicle');
  };

  const renderVehicle = ({ item }: { item: Vehicle }) => (
    <VehicleCard
      vehicle={item}
      onPress={() => handleVehiclePress(item.id)}
      onEdit={() => handleEditVehicle(item.id)}
      onDelete={() => handleDeleteVehicle(item)}
    />
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={vehicles}
        renderItem={renderVehicle}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContainer}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        showsVerticalScrollIndicator={false}
      />
      
      <FloatingActionButton onPress={handleAddVehicle} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  listContainer: {
    paddingVertical: 8,
    paddingBottom: 88, // Space for FAB
  },
});

export default VehicleListScreen;