
class Layer:
    
    def __init__(self, layer_type, parameters, is_divisible=False):
    
        self.layer_type = layer_type
        self.parameters = parameters
        self.is_divisible = is_divisible
        
    def is_computationally_intensive(self):
       
        # linear layers are good candidates for division
        # Conv2D layers with many parameters may be intensive but not good for division
        return self.layer_type in ['conv2d', 'linear'] and self.parameters > 1000
    
    def get_division_efficiency(self):
        # Linear layers are highly efficient for division
        if self.layer_type == 'linear' and self.is_divisible:
            return 0.9
        # Conv2D layers have high communication overhead when divided
        elif self.layer_type == 'conv2d':
            return 0.1
        # Other layers generally aren't worth dividing
        else:
            return 0
    
    def __repr__(self):
        divisible = "divisible" if self.is_divisible else "non-divisible"
        return f"Layer(type={self.layer_type}, params={self.parameters}, {divisible})"


class MLModel:
    
    def __init__(self, name, layers=None):
       
        self.name = name
        self.layers = layers or []
        self.total_parameters = sum(layer.parameters for layer in self.layers) if layers else 0
        
    def add_layer(self, layer):
        self.layers.append(layer)
        self.total_parameters += layer.parameters
        
    def get_layer(self, index):
       
        if 0 <= index < len(self.layers):
            return self.layers[index]
        return None
    
    def get_divisible_layers(self):
       
        return [(i, layer) for i, layer in enumerate(self.layers) 
                if layer.is_divisible and layer.get_division_efficiency() > 0.5]
    
    def __repr__(self):
        return f"MLModel(name={self.name}, layers={len(self.layers)}, params={self.total_parameters})"