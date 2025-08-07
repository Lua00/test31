import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const AddMaintenanceScreen: React.FC = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Bakım Ekleme Ekranı</Text>
      <Text style={styles.subText}>Bu ekran geliştirme aşamasındadır</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8fafc',
  },
  text: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
  },
  subText: {
    fontSize: 14,
    color: '#6b7280',
  },
});

export default AddMaintenanceScreen;