import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Alert,
  Image,
} from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { launchImageLibrary } from 'react-native-image-picker';

import { Vehicle } from '../types';
import { StorageService } from '../services/StorageService';

const EditVehicleScreen: React.FC = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { vehicleId } = route.params as { vehicleId: string };
  
  const [formData, setFormData] = useState({
    brand: '',
    model: '',
    year: '',
    licensePlate: '',
    currentKm: '',
    fuelType: 'gasoline' as Vehicle['fuelType'],
    engineSize: '',
    color: '',
    purchaseDate: '',
    imageUri: '',
  });

  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);

  const fuelTypes = [
    { value: 'gasoline', label: 'Benzin', icon: 'local-gas-station' },
    { value: 'diesel', label: 'Dizel', icon: 'local-gas-station' },
    { value: 'electric', label: 'Elektrik', icon: 'electric-car' },
    { value: 'hybrid', label: 'Hibrit', icon: 'eco' },
  ];

  useEffect(() => {
    loadVehicle();
  }, [vehicleId]);

  const loadVehicle = async () => {
    try {
      const vehicle = await StorageService.getVehicleById(vehicleId);
      if (vehicle) {
        setFormData({
          brand: vehicle.brand,
          model: vehicle.model,
          year: vehicle.year.toString(),
          licensePlate: vehicle.licensePlate,
          currentKm: vehicle.currentKm.toString(),
          fuelType: vehicle.fuelType,
          engineSize: vehicle.engineSize || '',
          color: vehicle.color || '',
          purchaseDate: vehicle.purchaseDate || '',
          imageUri: vehicle.imageUri || '',
        });
      }
    } catch (error) {
      console.error('Error loading vehicle:', error);
      Alert.alert('Hata', 'Araç bilgileri yüklenirken bir hata oluştu.');
    } finally {
      setInitialLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSelectImage = () => {
    launchImageLibrary(
      {
        mediaType: 'photo',
        quality: 0.8,
        maxWidth: 800,
        maxHeight: 600,
      },
      (response) => {
        if (response.assets && response.assets[0]) {
          setFormData(prev => ({
            ...prev,
            imageUri: response.assets![0].uri || '',
          }));
        }
      }
    );
  };

  const validateForm = () => {
    if (!formData.brand.trim()) {
      Alert.alert('Hata', 'Marka alanı zorunludur.');
      return false;
    }
    if (!formData.model.trim()) {
      Alert.alert('Hata', 'Model alanı zorunludur.');
      return false;
    }
    if (!formData.year.trim()) {
      Alert.alert('Hata', 'Yıl alanı zorunludur.');
      return false;
    }
    if (!formData.licensePlate.trim()) {
      Alert.alert('Hata', 'Plaka alanı zorunludur.');
      return false;
    }
    if (!formData.currentKm.trim()) {
      Alert.alert('Hata', 'Kilometre alanı zorunludur.');
      return false;
    }

    const year = parseInt(formData.year);
    if (isNaN(year) || year < 1900 || year > new Date().getFullYear() + 1) {
      Alert.alert('Hata', 'Geçerli bir yıl giriniz.');
      return false;
    }

    const km = parseInt(formData.currentKm);
    if (isNaN(km) || km < 0) {
      Alert.alert('Hata', 'Geçerli bir kilometre değeri giriniz.');
      return false;
    }

    return true;
  };

  const handleSave = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      const vehicle: Vehicle = {
        id: vehicleId,
        brand: formData.brand.trim(),
        model: formData.model.trim(),
        year: parseInt(formData.year),
        licensePlate: formData.licensePlate.trim().toUpperCase(),
        currentKm: parseInt(formData.currentKm),
        fuelType: formData.fuelType,
        engineSize: formData.engineSize.trim() || undefined,
        color: formData.color.trim() || undefined,
        purchaseDate: formData.purchaseDate.trim() || undefined,
        imageUri: formData.imageUri || undefined,
      };

      await StorageService.saveVehicle(vehicle);
      Alert.alert('Başarılı', 'Araç bilgileri güncellendi.', [
        {
          text: 'Tamam',
          onPress: () => navigation.goBack(),
        },
      ]);
    } catch (error) {
      console.error('Error updating vehicle:', error);
      Alert.alert('Hata', 'Araç güncellenirken bir hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  if (initialLoading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Yükleniyor...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.form}>
        {/* Image Selection */}
        <TouchableOpacity style={styles.imageSelector} onPress={handleSelectImage}>
          {formData.imageUri ? (
            <Image source={{ uri: formData.imageUri }} style={styles.selectedImage} />
          ) : (
            <View style={styles.imagePlaceholder}>
              <Icon name="add-a-photo" size={32} color="#9ca3af" />
              <Text style={styles.imagePlaceholderText}>Araç Fotoğrafı Ekle</Text>
            </View>
          )}
        </TouchableOpacity>

        {/* Basic Info */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Temel Bilgiler</Text>
          
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Marka *</Text>
            <TextInput
              style={styles.input}
              value={formData.brand}
              onChangeText={(value) => handleInputChange('brand', value)}
              placeholder="Örn: Honda"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Model *</Text>
            <TextInput
              style={styles.input}
              value={formData.model}
              onChangeText={(value) => handleInputChange('model', value)}
              placeholder="Örn: Civic"
            />
          </View>

          <View style={styles.row}>
            <View style={[styles.inputGroup, styles.flex1]}>
              <Text style={styles.label}>Yıl *</Text>
              <TextInput
                style={styles.input}
                value={formData.year}
                onChangeText={(value) => handleInputChange('year', value)}
                placeholder="2020"
                keyboardType="numeric"
              />
            </View>

            <View style={[styles.inputGroup, styles.flex1]}>
              <Text style={styles.label}>Renk</Text>
              <TextInput
                style={styles.input}
                value={formData.color}
                onChangeText={(value) => handleInputChange('color', value)}
                placeholder="Beyaz"
              />
            </View>
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Plaka *</Text>
            <TextInput
              style={styles.input}
              value={formData.licensePlate}
              onChangeText={(value) => handleInputChange('licensePlate', value)}
              placeholder="34 ABC 1234"
              autoCapitalize="characters"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Güncel Kilometre *</Text>
            <TextInput
              style={styles.input}
              value={formData.currentKm}
              onChangeText={(value) => handleInputChange('currentKm', value)}
              placeholder="42500"
              keyboardType="numeric"
            />
          </View>
        </View>

        {/* Fuel Type */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Yakıt Türü</Text>
          <View style={styles.fuelTypeContainer}>
            {fuelTypes.map((type) => (
              <TouchableOpacity
                key={type.value}
                style={[
                  styles.fuelTypeOption,
                  formData.fuelType === type.value && styles.fuelTypeSelected,
                ]}
                onPress={() => handleInputChange('fuelType', type.value)}>
                <Icon
                  name={type.icon}
                  size={20}
                  color={formData.fuelType === type.value ? '#ffffff' : '#6b7280'}
                />
                <Text
                  style={[
                    styles.fuelTypeText,
                    formData.fuelType === type.value && styles.fuelTypeTextSelected,
                  ]}>
                  {type.label}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Additional Info */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Ek Bilgiler</Text>
          
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Motor Hacmi</Text>
            <TextInput
              style={styles.input}
              value={formData.engineSize}
              onChangeText={(value) => handleInputChange('engineSize', value)}
              placeholder="1.6 L"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Satın Alma Tarihi</Text>
            <TextInput
              style={styles.input}
              value={formData.purchaseDate}
              onChangeText={(value) => handleInputChange('purchaseDate', value)}
              placeholder="01.01.2020"
            />
          </View>
        </View>

        <TouchableOpacity
          style={[styles.saveButton, loading && styles.saveButtonDisabled]}
          onPress={handleSave}
          disabled={loading}>
          <Text style={styles.saveButtonText}>
            {loading ? 'Güncelleniyor...' : 'Değişiklikleri Kaydet'}
          </Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
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
  form: {
    padding: 16,
  },
  imageSelector: {
    alignItems: 'center',
    marginBottom: 24,
  },
  selectedImage: {
    width: 200,
    height: 150,
    borderRadius: 12,
    resizeMode: 'cover',
  },
  imagePlaceholder: {
    width: 200,
    height: 150,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#d1d5db',
    borderStyle: 'dashed',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f9fafb',
  },
  imagePlaceholderText: {
    marginTop: 8,
    fontSize: 14,
    color: '#6b7280',
  },
  section: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 16,
  },
  inputGroup: {
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: '500',
    color: '#374151',
    marginBottom: 6,
  },
  input: {
    borderWidth: 1,
    borderColor: '#d1d5db',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    backgroundColor: '#ffffff',
  },
  row: {
    flexDirection: 'row',
    gap: 12,
  },
  flex1: {
    flex: 1,
  },
  fuelTypeContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  fuelTypeOption: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#d1d5db',
    backgroundColor: '#ffffff',
    gap: 8,
  },
  fuelTypeSelected: {
    backgroundColor: '#3b82f6',
    borderColor: '#3b82f6',
  },
  fuelTypeText: {
    fontSize: 14,
    color: '#6b7280',
  },
  fuelTypeTextSelected: {
    color: '#ffffff',
  },
  saveButton: {
    backgroundColor: '#3b82f6',
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  saveButtonDisabled: {
    backgroundColor: '#9ca3af',
  },
  saveButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default EditVehicleScreen;