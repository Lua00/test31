import AsyncStorage from '@react-native-async-storage/async-storage';
import { Vehicle, MaintenanceRecord } from '../types';

const VEHICLES_KEY = '@arcar_vehicles';
const MAINTENANCE_KEY = '@arcar_maintenance';

export class StorageService {
  // Vehicle operations
  static async getVehicles(): Promise<Vehicle[]> {
    try {
      const vehicles = await AsyncStorage.getItem(VEHICLES_KEY);
      return vehicles ? JSON.parse(vehicles) : [];
    } catch (error) {
      console.error('Error getting vehicles:', error);
      return [];
    }
  }

  static async saveVehicle(vehicle: Vehicle): Promise<void> {
    try {
      const vehicles = await this.getVehicles();
      const existingIndex = vehicles.findIndex(v => v.id === vehicle.id);
      
      if (existingIndex >= 0) {
        vehicles[existingIndex] = vehicle;
      } else {
        vehicles.push(vehicle);
      }
      
      await AsyncStorage.setItem(VEHICLES_KEY, JSON.stringify(vehicles));
    } catch (error) {
      console.error('Error saving vehicle:', error);
      throw error;
    }
  }

  static async deleteVehicle(vehicleId: string): Promise<void> {
    try {
      const vehicles = await this.getVehicles();
      const filteredVehicles = vehicles.filter(v => v.id !== vehicleId);
      await AsyncStorage.setItem(VEHICLES_KEY, JSON.stringify(filteredVehicles));
      
      // Also delete related maintenance records
      await this.deleteMaintenanceRecordsByVehicle(vehicleId);
    } catch (error) {
      console.error('Error deleting vehicle:', error);
      throw error;
    }
  }

  static async getVehicleById(vehicleId: string): Promise<Vehicle | null> {
    try {
      const vehicles = await this.getVehicles();
      return vehicles.find(v => v.id === vehicleId) || null;
    } catch (error) {
      console.error('Error getting vehicle by id:', error);
      return null;
    }
  }

  // Maintenance operations
  static async getMaintenanceRecords(): Promise<MaintenanceRecord[]> {
    try {
      const records = await AsyncStorage.getItem(MAINTENANCE_KEY);
      return records ? JSON.parse(records) : [];
    } catch (error) {
      console.error('Error getting maintenance records:', error);
      return [];
    }
  }

  static async getMaintenanceRecordsByVehicle(vehicleId: string): Promise<MaintenanceRecord[]> {
    try {
      const records = await this.getMaintenanceRecords();
      return records.filter(r => r.vehicleId === vehicleId).sort((a, b) => 
        new Date(b.date).getTime() - new Date(a.date).getTime()
      );
    } catch (error) {
      console.error('Error getting maintenance records by vehicle:', error);
      return [];
    }
  }

  static async saveMaintenanceRecord(record: MaintenanceRecord): Promise<void> {
    try {
      const records = await this.getMaintenanceRecords();
      const existingIndex = records.findIndex(r => r.id === record.id);
      
      if (existingIndex >= 0) {
        records[existingIndex] = record;
      } else {
        records.push(record);
      }
      
      await AsyncStorage.setItem(MAINTENANCE_KEY, JSON.stringify(records));
    } catch (error) {
      console.error('Error saving maintenance record:', error);
      throw error;
    }
  }

  static async deleteMaintenanceRecord(recordId: string): Promise<void> {
    try {
      const records = await this.getMaintenanceRecords();
      const filteredRecords = records.filter(r => r.id !== recordId);
      await AsyncStorage.setItem(MAINTENANCE_KEY, JSON.stringify(filteredRecords));
    } catch (error) {
      console.error('Error deleting maintenance record:', error);
      throw error;
    }
  }

  static async deleteMaintenanceRecordsByVehicle(vehicleId: string): Promise<void> {
    try {
      const records = await this.getMaintenanceRecords();
      const filteredRecords = records.filter(r => r.vehicleId !== vehicleId);
      await AsyncStorage.setItem(MAINTENANCE_KEY, JSON.stringify(filteredRecords));
    } catch (error) {
      console.error('Error deleting maintenance records by vehicle:', error);
      throw error;
    }
  }

  static async getMaintenanceRecordById(recordId: string): Promise<MaintenanceRecord | null> {
    try {
      const records = await this.getMaintenanceRecords();
      return records.find(r => r.id === recordId) || null;
    } catch (error) {
      console.error('Error getting maintenance record by id:', error);
      return null;
    }
  }

  // Utility methods
  static async clearAllData(): Promise<void> {
    try {
      await AsyncStorage.multiRemove([VEHICLES_KEY, MAINTENANCE_KEY]);
    } catch (error) {
      console.error('Error clearing all data:', error);
      throw error;
    }
  }
}