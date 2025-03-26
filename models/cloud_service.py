
import time
import random

class CloudService:
    
    def __init__(self, latency_range=(0.1, 0.3)):
        """
         latency_range (tuple): Min and max network latency in seconds
        """
        self.model = None
        self.available = True
        self.latency_range = latency_range
        self.success_rate = 0.95  # 95% chance of successful connection
    
    def execute_task(self, task):
        """
        Args:
            task: The task to execute
            
        Returns:
            dict: Results and performance metrics or None if connection fails
        """
        if not self.check_availability():
            return None
            
        start_time = time.time()
        
        # Simulate network latency
        network_latency = random.uniform(*self.latency_range)
        time.sleep(network_latency)
        
        # Simulate cloud processing (faster than edge)
        time.sleep(0.05)
        
        # Simulate return network latency
        time.sleep(network_latency)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            "result": {"status": "completed", "source": "cloud"},
            "execution_time": execution_time,
            "network_latency": network_latency * 2  # Round trip
        }
    
    def check_availability(self):
        # Simulate occasional cloud unavailability
        self.available = random.random() < self.success_rate
        return self.available
    
    def __repr__(self):
        status = "available" if self.available else "unavailable"
        return f"CloudService(status={status})"