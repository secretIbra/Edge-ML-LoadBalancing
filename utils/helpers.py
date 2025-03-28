
import time
import random
import json
import os

def get_current_time():
    
    return time.time()

def format_time(timestamp):
   
    import datetime
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def generate_random_image_data(size=(224, 224, 3)):
    
    return {
        "data": f"random_image_data_{random.randint(1000, 9999)}",
        "size": size
    }

def load_config(config_file="config.json"):
   
    if not os.path.exists(config_file):
        return {}
        
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

def save_results(results, filename="results.json"):
   
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving results: {e}")
        return False

def create_alexnet_model():
    
    from models.ml_model import MLModel, Layer
    
    model = MLModel("AlexNet")
    
    # Convolutional layers
    model.add_layer(Layer("conv2d", 23296, is_divisible=False))
    model.add_layer(Layer("conv2d", 307456, is_divisible=False))
    model.add_layer(Layer("conv2d", 663936, is_divisible=False))
    model.add_layer(Layer("conv2d", 885120, is_divisible=False))
    model.add_layer(Layer("conv2d", 590080, is_divisible=False))
    
    # Fully connected layers (divisible)
    model.add_layer(Layer("linear", 37752832, is_divisible=True))
    model.add_layer(Layer("linear", 16781312, is_divisible=True))
    model.add_layer(Layer("linear", 4097000, is_divisible=True))
    
    return model

def create_vgg11_model():
    
    from models.ml_model import MLModel, Layer
    
    model = MLModel("VGG11")
    
    # Convolutional layers
    model.add_layer(Layer("conv2d", 1792, is_divisible=False))
    model.add_layer(Layer("conv2d", 36928, is_divisible=False))
    model.add_layer(Layer("conv2d", 73856, is_divisible=False))
    model.add_layer(Layer("conv2d", 147584, is_divisible=False))
    model.add_layer(Layer("conv2d", 295168, is_divisible=False))
    model.add_layer(Layer("conv2d", 590080, is_divisible=False))
    model.add_layer(Layer("conv2d", 590080, is_divisible=False))
    model.add_layer(Layer("conv2d", 590080, is_divisible=False))
    
    # Fully connected layers (divisible)
    model.add_layer(Layer("linear", 102764544, is_divisible=True))
    model.add_layer(Layer("linear", 16781312, is_divisible=True))
    model.add_layer(Layer("linear", 4097000, is_divisible=True))
    
    return model