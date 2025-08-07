import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import LinearGradient from 'react-native-linear-gradient';

import { Vehicle, MaintenanceRecord } from '../types';
import { StorageService } from '../services/StorageService';
import MaintenanceCard from '../components/MaintenanceCard';
import FloatingActionButton from '../components/FloatingActionButton';

const VehicleDetailScreen: React.FC = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { vehicleId } = route.params as { vehicleId: string };

  const [vehicle, setVehicle] = useState<Vehicle | null>(null);
  const [maintenanceRecords, setMaintenanceRecords] = useState<MaintenanceRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadVehicleData();
  }, [vehicleId]);

  const loadVehicleData = async () => {
    try {
      const [vehicleData, maintenanceData] = await Promise.all([
        StorageService.getVehicleById(vehicleId),
        StorageService.getMaintenanceRecordsByVehicle(vehicleId),
      ]);
      
      setVehicle(vehicleData);
      setMaintenanceRecords(maintenanceData);
    } catch (error) {
      console.error('Error loading vehicle data:', error);
      Alert.alert('Hata', 'Araç bilgileri yüklenirken bir hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddMaintenance = () => {
    navigation.navigate('AddMaintenance', { vehicleId });
  };

  const handleEditVehicle = () => {
    navigation.navigate('EditVehicle', { vehicleId });
  };

  const handleMaintenancePress = (maintenanceId: string) => {
    navigation.navigate('MaintenanceDetail', { maintenanceId });
  };

  const getFuelTypeInfo = (fuelType: string) => {
    switch (fuelType) {
      case 'gasoline':
        return { name: 'Benzin', icon: 'local-gas-station', color: '#f59e0b' };
      case 'diesel':
        return { name: 'Dizel', icon: 'local-gas-station', color: '#6b7280' };
      case 'electric':
        return { name: 'Elektrik', icon: 'electric-car', color: '#10b981' };
      case 'hybrid':
        return { name: 'Hibrit', icon: 'eco', color: '#3b82f6' };
      default:
        return { name: 'Bilinmiyor', icon: 'help', color: '#6b7280' };
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Yükleniyor...</Text>
      </View>
    );
  }

  if (!vehicle) {
    return (
      <View style={styles.errorContainer}>
        <Icon name="error" size={64} color="#ef4444" />
        <Text style={styles.errorText}>Araç bulunamadı</Text>
      </View>
    );
  }

  const fuelInfo = getFuelTypeInfo(vehicle.fuelType);

  return (
    <View style={styles.container}>
      <ScrollView style={styles.content}>
        {/* Header Section */}
        <LinearGradient
          colors={['#3b82f6', '#2563eb']}
          style={styles.header}>
          <TouchableOpacity
            style={styles.editButton}
            onPress={handleEditVehicle}>
            <Icon name="edit" size={20} color="#ffffff" />
          </TouchableOpacity>
          
          <View style={styles.headerContent}>
            <Text style={styles.brandModel}>
              {vehicle.brand} {vehicle.model}
            </Text>
            <Text style={styles.year}>{vehicle.year}</Text>
            
            <View style={styles.plateContainer}>
              <View style={styles.plate}>
                <Text style={styles.plateText}>{vehicle.licensePlate}</Text>
              </View>
            </View>
          </View>
        </LinearGradient>

        {/* Vehicle Image */}
        {vehicle.imageUri && (
          <View style={styles.imageContainer}>
            <Image source={{ uri: vehicle.imageUri }} style={styles.vehicleImage} />
          </View>
        )}

        {/* Vehicle Info */}
        <View style={styles.infoSection}>
          <Text style={styles.sectionTitle}>Araç Bilgileri</Text>
          
          <View style={styles.infoGrid}>
            <View style={styles.infoItem}>
              <Icon name="speed" size={24} color="#6b7280" />
              <Text style={styles.infoLabel}>Kilometre</Text>
              <Text style={styles.infoValue}>
                {vehicle.currentKm.toLocaleString('tr-TR')} km
              </Text>
            </View>

            <View style={styles.infoItem}>
              <Icon name={fuelInfo.icon} size={24} color={fuelInfo.color} />
              <Text style={styles.infoLabel}>Yakıt Türü</Text>
              <Text style={styles.infoValue}>{fuelInfo.name}</Text>
            </View>

            {vehicle.engineSize && (
              <View style={styles.infoItem}>
                <Icon name="settings" size={24} color="#6b7280" />
                <Text style={styles.infoLabel}>Motor Hacmi</Text>
                <Text style={styles.infoValue}>{vehicle.engineSize}</Text>
              </View>
            )}

            {vehicle.color && (
              <View style={styles.infoItem}>
                <Icon name="palette" size={24} color="#6b7280" />
                <Text style={styles.infoLabel}>Renk</Text>
                <Text style={styles.infoValue}>{vehicle.color}</Text>
              </View>
            )}

            {vehicle.purchaseDate && (
              <View style={styles.infoItem}>
                <Icon name="event" size={24} color="#6b7280" />
                <Text style={styles.infoLabel}>Satın Alma</Text>
                <Text style={styles.infoValue}>{vehicle.purchaseDate}</Text>
              </View>
            )}
          </View>
        </View>

        {/* Maintenance Records */}
        <View style={styles.maintenanceSection}>
          <View style={styles.maintenanceHeader}>
            <Text style={styles.sectionTitle}>Bakım/Tamir Geçmişi</Text>
            <Text style={styles.recordCount}>
              {maintenanceRecords.length} kayıt
            </Text>
          </View>
          
          {maintenanceRecords.length > 0 ? (
            maintenanceRecords.map((record) => (
              <MaintenanceCard
                key={record.id}
                record={record}
                onPress={() => handleMaintenancePress(record.id)}
              />
            ))
          ) : (
            <View style={styles.emptyState}>
              <Icon name="build" size={48} color="#9ca3af" />
              <Text style={styles.emptyTitle}>Henüz bakım kaydı yok</Text>
              <Text style={styles.emptyDescription}>
                İlk bakım/tamir kaydınızı eklemek için + butonuna dokunun
              </Text>
            </View>
          )}
        </View>

        <View style={styles.bottomPadding} />
      </ScrollView>

      <FloatingActionButton
        onPress={handleAddMaintenance}
        iconName="build"
        colors={['#10b981', '#059669']}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  content: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8fafc',
  },
  loadingText: {
    fontSize: 16,
    color: '#6b7280',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8fafc',
  },
  errorText: {
    fontSize: 18,
    color: '#6b7280',
    marginTop: 16,
  },
  header: {
    paddingTop: 20,
    paddingBottom: 24,
    paddingHorizontal: 20,
    position: 'relative',
  },
  editButton: {
    position: 'absolute',
    top: 20,
    right: 20,
    padding: 8,
    borderRadius: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  headerContent: {
    alignItems: 'center',
    marginTop: 40,
  },
  brandModel: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 4,
  },
  year: {
    fontSize: 16,
    color: '#dbeafe',
    marginBottom: 16,
  },
  plateContainer: {
    alignItems: 'center',
  },
  plate: {
    backgroundColor: '#1f2937',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: '#374151',
  },
  plateText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 2,
  },
  imageContainer: {
    alignItems: 'center',
    paddingVertical: 20,
  },
  vehicleImage: {
    width: '90%',
    height: 200,
    borderRadius: 12,
    resizeMode: 'cover',
  },
  infoSection: {
    backgroundColor: '#ffffff',
    marginHorizontal: 16,
    marginVertical: 8,
    borderRadius: 12,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.05,
    shadowRadius: 4,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 16,
  },
  infoGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 16,
  },
  infoItem: {
    alignItems: 'center',
    minWidth: '45%',
    marginBottom: 16,
  },
  infoLabel: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 6,
    marginBottom: 2,
  },
  infoValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1f2937',
  },
  maintenanceSection: {
    marginTop: 8,
  },
  maintenanceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    marginBottom: 16,
  },
  recordCount: {
    fontSize: 14,
    color: '#6b7280',
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 48,
    paddingHorizontal: 32,
  },
  emptyTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#4b5563',
    marginTop: 12,
    marginBottom: 8,
  },
  emptyDescription: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 20,
  },
  bottomPadding: {
    height: 88,
  },
});

export default VehicleDetailScreen;