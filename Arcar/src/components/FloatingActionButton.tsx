import React from 'react';
import {
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import LinearGradient from 'react-native-linear-gradient';

interface FloatingActionButtonProps {
  onPress: () => void;
  iconName?: string;
  colors?: string[];
}

const FloatingActionButton: React.FC<FloatingActionButtonProps> = ({
  onPress,
  iconName = 'add',
  colors = ['#3b82f6', '#2563eb'],
}) => {
  return (
    <TouchableOpacity
      style={styles.container}
      onPress={onPress}
      activeOpacity={0.8}>
      <LinearGradient
        colors={colors}
        style={styles.gradient}>
        <Icon name={iconName} size={24} color="#ffffff" />
      </LinearGradient>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    bottom: 24,
    right: 24,
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  gradient: {
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default FloatingActionButton;