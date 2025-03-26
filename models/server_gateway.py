
import time

class ServerGateway:
    """Handles communication between edge devices and cloud."""
    
    def __init__(self, cloud_service):
        
        self.cloud_service = cloud_service
        self.connected_edge_devices = []
        self.last_cloud_request = 0
        self.request_timeout = 10  # seconds
    
    def register_edge_device(self, device):
       
        if device not in self.connected_edge_devices:
            self.connected_edge_devices.append(device)
            return True
        return False
    
    def send_to_cloud(self, task, source_device):
        
        current_time = time.time()
        
        # Rate limiting to prevent overwhelming the cloud
        if current_time - self.last_cloud_request < 0.1:
            time.sleep(0.1)
        
        self.last_cloud_request = time.time()
        
        if not self.cloud_service.check_availability():
            return {"error": "Cloud service unavailable"}
        
        result = self.cloud_service.execute_task(task)
        
        if result is None:
            return {"error": "Failed to execute task in cloud"}
        
        return result
    
    def send_to_edge(self, result, target_device):
        # In a real implementation, this would handle network communication
        # For now, we'll just simulate success
        return True
    
    def __repr__(self):
        return f"ServerGateway(connected_devices={len(self.connected_edge_devices)})"