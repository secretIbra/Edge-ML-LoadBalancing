
class HorizontalLoadBalancer:
    
    def __init__(self, root_device):
        self.root_device = root_device
        
    def get_connected_devices(self):
       
        return [self.root_device] + self.root_device.connected_devices
        
    def calculate_distribution(self):
        """
        Calculate workload distribution based on computational power.
        
        Returns:
            dict: Mapping of device IDs to power ratios
        """
        devices = self.get_connected_devices()
        
        # Update CPU usage for all devices
        for device in devices:
            device.update_cpu_usage()
        
        # Calculate total power
        powers = {device.device_id: device.get_computational_power() for device in devices}
        total_power = sum(powers.values())
        
        if total_power == 0:
            # Fallback if total power is 0
            num_devices = len(devices)
            return {device.device_id: 1/num_devices for device in devices}
        
        # Calculate distribution ratio
        distribution = {device_id: power/total_power for device_id, power in powers.items()}
        return distribution
        
    def distribute_layer(self, layer, model):
        """
        Distribute a layer's computation across devices.
        
        Args:
            layer: The layer to distribute
            model: The model containing the layer
            
        Returns:
            dict: Mapping of device IDs to parameter ranges (start, end)
        """
        # Only divide divisible layers (like linear layers)
        if not layer.is_divisible:
            return {self.root_device.device_id: (0, layer.parameters)}
            
        distribution = self.calculate_distribution()
        devices = self.get_connected_devices()
        device_map = {}
        
        start_idx = 0
        for device in devices:
            param_count = int(layer.parameters * distribution[device.device_id])
            # Ensure at least 1 parameter per device
            param_count = max(1, param_count)
            end_idx = start_idx + param_count
            
            # Ensure we don't exceed layer parameters
            end_idx = min(end_idx, layer.parameters)
            
            device_map[device.device_id] = (start_idx, end_idx)
            start_idx = end_idx
            
            # If we've covered all parameters, stop
            if end_idx >= layer.parameters:
                break
                
        return device_map
        
    def distribute_layers(self, model):
        """
        Distribute entire model layers across devices without dividing layers.
        
        Args:
            model: The model to distribute
            
        Returns:
            dict: Mapping of device IDs to layer indices
        """
        distribution = self.calculate_distribution()
        devices = self.get_connected_devices()
        device_to_layers = {device.device_id: [] for device in devices}
        
        # Assign layers proportionally to computational power
        total_layers = len(model.layers)
        assigned = 0
        
        for device in devices:
            # Calculate layer count based on power distribution
            layer_count = int(total_layers * distribution[device.device_id])
            # Ensure at least 1 layer per device if possible
            layer_count = max(1, layer_count)
            
            # Last device gets remaining layers
            if device == devices[-1]:
                layer_count = total_layers - assigned
                
            # Assign layer indices
            device_to_layers[device.device_id] = list(range(assigned, min(assigned + layer_count, total_layers)))
            assigned += layer_count
            
            # If we've assigned all layers, stop
            if assigned >= total_layers:
                break
                
        return device_to_layers
    
    def __repr__(self):
        devices = len(self.get_connected_devices())
        return f"HorizontalLoadBalancer(connected_devices={devices})"