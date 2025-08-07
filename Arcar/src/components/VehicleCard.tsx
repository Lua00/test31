import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Image,
  Dimensions,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import LinearGradient from 'react-native-linear-gradient';
import { Vehicle } from '../types';

interface VehicleCardProps {
  vehicle: Vehicle;
  onPress: () => void;
  onEdit?: () => void;
  onDelete?: () => void;
}

const { width } = Dimensions.get('window');

const VehicleCard: React.FC<VehicleCardProps> = ({
  vehicle,
  onPress,
  onEdit,
  onDelete,
}) => {
  const getFuelTypeIcon = (fuelType: string) => {
    switch (fuelType) {
      case 'gasoline':
        return 'local-gas-station';
      case 'diesel':
        return 'local-gas-station';
      case 'electric':
        return 'electric-car';
      case 'hybrid':
        return 'eco';
      default:
        return 'local-gas-station';
    }
  };

  const getFuelTypeColor = (fuelType: string) => {
    switch (fuelType) {
      case 'gasoline':
        return '#f59e0b';
      case 'diesel':
        return '#6b7280';
      case 'electric':
        return '#10b981';
      case 'hybrid':
        return '#3b82f6';
      default:
        return '#6b7280';
    }
  };

  return (
    <TouchableOpacity
      style={styles.container}
      onPress={onPress}
      activeOpacity={0.8}>
      <LinearGradient
        colors={['#ffffff', '#f8fafc']}
        style={styles.gradient}>
        <View style={styles.header}>
          <View style={styles.vehicleInfo}>
            <Text style={styles.brandModel}>
              {vehicle.brand} {vehicle.model}
            </Text>
            <Text style={styles.year}>{vehicle.year}</Text>
          </View>
          {(onEdit || onDelete) && (
            <View style={styles.actions}>
              {onEdit && (
                <TouchableOpacity
                  style={styles.actionButton}
                  onPress={onEdit}>
                  <Icon name="edit" size={20} color="#6b7280" />
                </TouchableOpacity>
              )}
              {onDelete && (
                <TouchableOpacity
                  style={styles.actionButton}
                  onPress={onDelete}>
                  <Icon name="delete" size={20} color="#ef4444" />
                </TouchableOpacity>
              )}
            </View>
          )}
        </View>

        <View style={styles.plateContainer}>
          <View style={styles.plate}>
            <Text style={styles.plateText}>{vehicle.licensePlate}</Text>
          </View>
        </View>

        <View style={styles.details}>
          <View style={styles.detailItem}>
            <Icon name="speed" size={18} color="#6b7280" />
            <Text style={styles.detailText}>
              {vehicle.currentKm.toLocaleString('tr-TR')} km
            </Text>
          </View>
          
          <View style={styles.detailItem}>
            <Icon 
              name={getFuelTypeIcon(vehicle.fuelType)} 
              size={18} 
              color={getFuelTypeColor(vehicle.fuelType)} 
            />
            <Text style={styles.detailText}>
              {vehicle.fuelType === 'gasoline' ? 'Benzin' : 
               vehicle.fuelType === 'diesel' ? 'Dizel' : 
               vehicle.fuelType === 'electric' ? 'Elektrik' : 'Hibrit'}
            </Text>
          </View>
        </View>

        {vehicle.imageUri && (
          <View style={styles.imageContainer}>
            <Image source={{ uri: vehicle.imageUri }} style={styles.image} />
          </View>
        )}

        <View style={styles.footer}>
          <Icon name="arrow-forward-ios" size={16} color="#9ca3af" />
        </View>
      </LinearGradient>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    marginHorizontal: 16,
    marginVertical: 8,
    borderRadius: 16,
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  gradient: {
    borderRadius: 16,
    padding: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  vehicleInfo: {
    flex: 1,
  },
  brandModel: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 4,
  },
  year: {
    fontSize: 14,
    color: '#6b7280',
  },
  actions: {
    flexDirection: 'row',
    gap: 8,
  },
  actionButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#f3f4f6',
  },
  plateContainer: {
    alignItems: 'center',
    marginBottom: 16,
  },
  plate: {
    backgroundColor: '#1f2937',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: '#374151',
  },
  plateText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
    letterSpacing: 2,
  },
  details: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 16,
  },
  detailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  detailText: {
    fontSize: 14,
    color: '#4b5563',
    fontWeight: '500',
  },
  imageContainer: {
    alignItems: 'center',
    marginBottom: 16,
  },
  image: {
    width: width * 0.7,
    height: 120,
    borderRadius: 12,
    resizeMode: 'cover',
  },
  footer: {
    alignItems: 'flex-end',
  },
});

export default VehicleCard;