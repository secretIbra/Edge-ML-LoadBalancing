
import time
import psutil  # For CPU usage monitoring

class EdgeDevice:
    
    def __init__(self, device_id, cpu_speed, num_cores, is_root=False):
       
        self.device_id = device_id
        self.cpu_speed = cpu_speed
        self.num_cores = num_cores
        self.is_root = is_root
        self.current_cpu_usage = 0
        self.available_memory = 0
        self.connected_devices = []
        self.model = None
    
    def get_computational_power(self):
        return self.cpu_speed * self.num_cores * (1 - self.current_cpu_usage/100)
    
    def update_cpu_usage(self):
        self.current_cpu_usage = psutil.cpu_percent(interval=0.1)
        return self.current_cpu_usage
    
    def execute_task(self, task, layer_indices=None):
        start_time = time.time()
        
        # Record CPU before execution
        cpu_before = self.update_cpu_usage()
        
        # Task execution logic will go here
        result = {"status": "completed", "device": self.device_id}
        
        # Simulate processing time
        time.sleep(0.1)
        
        # Record CPU after execution
        cpu_after = self.update_cpu_usage()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            "result": result,
            "execution_time": execution_time,
            "cpu_before": cpu_before,
            "cpu_after": cpu_after
        }
    
    def connect_to_device(self, device):

        if device not in self.connected_devices:
            self.connected_devices.append(device)
            return True
        return False
    
    def __repr__(self):
        return f"EdgeDevice(id={self.device_id}, cores={self.num_cores}, speed={self.cpu_speed}GHz)"