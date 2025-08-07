import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Image,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { MaintenanceRecord } from '../types';

interface MaintenanceCardProps {
  record: MaintenanceRecord;
  onPress: () => void;
}

const MaintenanceCard: React.FC<MaintenanceCardProps> = ({ record, onPress }) => {
  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'oil_change':
        return 'oil-barrel';
      case 'tire_change':
        return 'tire-repair';
      case 'brake_service':
        return 'car-brake-alert';
      case 'engine_repair':
        return 'engine';
      default:
        return 'build';
    }
  };

  const getCategoryName = (category: string) => {
    switch (category) {
      case 'oil_change':
        return 'Yağ Değişimi';
      case 'tire_change':
        return 'Lastik Değişimi';
      case 'brake_service':
        return 'Fren Bakımı';
      case 'engine_repair':
        return 'Motor Tamiri';
      default:
        return 'Diğer';
    }
  };

  const getTypeColor = (type: string) => {
    return type === 'maintenance' ? '#10b981' : '#f59e0b';
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('tr-TR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  return (
    <TouchableOpacity
      style={styles.container}
      onPress={onPress}
      activeOpacity={0.8}>
      <View style={styles.header}>
        <View style={styles.typeIndicator}>
          <View 
            style={[
              styles.typeBadge, 
              { backgroundColor: getTypeColor(record.type) }
            ]}>
            <Text style={styles.typeText}>
              {record.type === 'maintenance' ? 'BAKIM' : 'TAMİR'}
            </Text>
          </View>
        </View>
        <Text style={styles.date}>{formatDate(record.date)}</Text>
      </View>

      <View style={styles.content}>
        <View style={styles.categoryContainer}>
          <Icon 
            name={getCategoryIcon(record.category)} 
            size={24} 
            color="#6b7280" 
          />
          <Text style={styles.categoryText}>
            {getCategoryName(record.category)}
          </Text>
        </View>

        <Text style={styles.description} numberOfLines={2}>
          {record.description}
        </Text>

        <View style={styles.details}>
          <View style={styles.detailItem}>
            <Icon name="speed" size={16} color="#6b7280" />
            <Text style={styles.detailText}>
              {record.kilometerage.toLocaleString('tr-TR')} km
            </Text>
          </View>
          
          {record.cost && (
            <View style={styles.detailItem}>
              <Icon name="attach-money" size={16} color="#6b7280" />
              <Text style={styles.detailText}>
                {record.cost.toLocaleString('tr-TR')} ₺
              </Text>
            </View>
          )}
        </View>

        {record.imageUri && (
          <View style={styles.imageContainer}>
            <Image source={{ uri: record.imageUri }} style={styles.image} />
          </View>
        )}
      </View>

      <View style={styles.footer}>
        <Icon name="arrow-forward-ios" size={14} color="#9ca3af" />
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#ffffff',
    marginHorizontal: 16,
    marginVertical: 6,
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
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  typeIndicator: {
    flexDirection: 'row',
  },
  typeBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  typeText: {
    color: '#ffffff',
    fontSize: 10,
    fontWeight: 'bold',
  },
  date: {
    fontSize: 12,
    color: '#6b7280',
    fontWeight: '500',
  },
  content: {
    marginBottom: 12,
  },
  categoryContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 8,
  },
  categoryText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
  },
  description: {
    fontSize: 14,
    color: '#4b5563',
    lineHeight: 20,
    marginBottom: 12,
  },
  details: {
    flexDirection: 'row',
    gap: 16,
    marginBottom: 8,
  },
  detailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  detailText: {
    fontSize: 12,
    color: '#6b7280',
    fontWeight: '500',
  },
  imageContainer: {
    alignItems: 'center',
    marginTop: 8,
  },
  image: {
    width: 80,
    height: 80,
    borderRadius: 8,
    resizeMode: 'cover',
  },
  footer: {
    alignItems: 'flex-end',
  },
});

export default MaintenanceCard;