import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { RootStackParamList } from '../types';
import HomeScreen from '../screens/HomeScreen';
import VehicleListScreen from '../screens/VehicleListScreen';
import VehicleDetailScreen from '../screens/VehicleDetailScreen';
import AddVehicleScreen from '../screens/AddVehicleScreen';
import EditVehicleScreen from '../screens/EditVehicleScreen';
import MaintenanceListScreen from '../screens/MaintenanceListScreen';
import AddMaintenanceScreen from '../screens/AddMaintenanceScreen';
import MaintenanceDetailScreen from '../screens/MaintenanceDetailScreen';

const Stack = createStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator();

const VehicleStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerStyle: {
        backgroundColor: '#2563eb',
      },
      headerTintColor: '#ffffff',
      headerTitleStyle: {
        fontWeight: 'bold',
      },
    }}>
    <Stack.Screen 
      name="VehicleList" 
      component={VehicleListScreen}
      options={{ title: 'Araçlarım' }}
    />
    <Stack.Screen 
      name="VehicleDetail" 
      component={VehicleDetailScreen}
      options={{ title: 'Araç Detayı' }}
    />
    <Stack.Screen 
      name="AddVehicle" 
      component={AddVehicleScreen}
      options={{ title: 'Araç Ekle' }}
    />
    <Stack.Screen 
      name="EditVehicle" 
      component={EditVehicleScreen}
      options={{ title: 'Araç Düzenle' }}
    />
    <Stack.Screen 
      name="MaintenanceList" 
      component={MaintenanceListScreen}
      options={{ title: 'Bakım/Tamir Geçmişi' }}
    />
    <Stack.Screen 
      name="AddMaintenance" 
      component={AddMaintenanceScreen}
      options={{ title: 'Bakım/Tamir Ekle' }}
    />
    <Stack.Screen 
      name="MaintenanceDetail" 
      component={MaintenanceDetailScreen}
      options={{ title: 'Bakım/Tamir Detayı' }}
    />
  </Stack.Navigator>
);

const TabNavigator = () => (
  <Tab.Navigator
    screenOptions={({ route }) => ({
      tabBarIcon: ({ focused, color, size }) => {
        let iconName = '';

        if (route.name === 'Home') {
          iconName = 'home';
        } else if (route.name === 'VehicleStack') {
          iconName = 'directions-car';
        }

        return <Icon name={iconName} size={size} color={color} />;
      },
      tabBarActiveTintColor: '#2563eb',
      tabBarInactiveTintColor: 'gray',
      headerShown: false,
    })}>
    <Tab.Screen 
      name="Home" 
      component={HomeScreen}
      options={{ title: 'Ana Sayfa' }}
    />
    <Tab.Screen 
      name="VehicleStack" 
      component={VehicleStack}
      options={{ title: 'Araçlar' }}
    />
  </Tab.Navigator>
);

const AppNavigator = () => {
  return (
    <NavigationContainer>
      <TabNavigator />
    </NavigationContainer>
  );
};

export default AppNavigator;