export interface Vehicle {
  id: string;
  brand: string;
  model: string;
  year: number;
  licensePlate: string;
  currentKm: number;
  fuelType: 'gasoline' | 'diesel' | 'hybrid' | 'electric';
  engineSize?: string;
  color?: string;
  purchaseDate?: string;
  imageUri?: string;
}

export interface MaintenanceRecord {
  id: string;
  vehicleId: string;
  type: 'maintenance' | 'repair';
  category: 'oil_change' | 'tire_change' | 'brake_service' | 'engine_repair' | 'other';
  description: string;
  date: string;
  kilometerage: number;
  cost?: number;
  notes?: string;
  imageUri?: string;
  nextMaintenanceKm?: number;
  nextMaintenanceDate?: string;
}

export interface MaintenanceType {
  id: string;
  name: string;
  icon: string;
  color: string;
  category: 'maintenance' | 'repair';
}

export type RootStackParamList = {
  Home: undefined;
  VehicleList: undefined;
  VehicleDetail: { vehicleId: string };
  AddVehicle: undefined;
  EditVehicle: { vehicleId: string };
  MaintenanceList: { vehicleId: string };
  AddMaintenance: { vehicleId: string };
  MaintenanceDetail: { maintenanceId: string };
};