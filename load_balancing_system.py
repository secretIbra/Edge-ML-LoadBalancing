
import time
import random
from models.edge_device import EdgeDevice
from models.cloud_service import CloudService
from models.server_gateway import ServerGateway
from models.ml_model import MLModel, Layer
from models.task import Task
from load_balancers.vertical_balancer import VerticalLoadBalancer
from load_balancers.horizontal_balancer import HorizontalLoadBalancer
from monitoring.system_monitor import SystemMonitor
from utils.helpers import get_current_time, generate_random_image_data

class LoadBalancingSystem:
    """Main system that orchestrates the entire load balancing process."""
    
    def __init__(self):
        # Initialize components
        self.cloud_service = CloudService()
        self.server_gateway = ServerGateway(self.cloud_service)
        self.root_device = EdgeDevice(device_id="root", cpu_speed=1.4, num_cores=4, is_root=True)
        self.vertical_balancer = VerticalLoadBalancer(self.root_device, self.server_gateway)
        self.horizontal_balancer = HorizontalLoadBalancer(self.root_device)
        self.system_monitor = SystemMonitor()
        self.task_queue = []
        
    def add_edge_device(self, device_id, cpu_speed, num_cores):
       
        device = EdgeDevice(device_id, cpu_speed, num_cores)
        self.root_device.connect_to_device(device)
        self.server_gateway.register_edge_device(device)
        return device
        
    def load_model(self, model):
       
        self.root_device.model = model
        
    def create_task(self, input_data=None, deadline=None, is_sensitive=False):
       
        task_id = f"task_{len(self.task_queue) + 1}"
        
        # Generate random data if none provided
        if input_data is None:
            input_data = generate_random_image_data()
            
        # Generate random deadline if none provided
        if deadline is None:
            deadline = random.uniform(0.5, 10)
            
        task = Task(task_id, input_data, deadline, is_sensitive)
        self.task_queue.append(task)
        return task
        
    def process_task(self, task, balancing_condition="cpu"):
       
        # Record CPU before task
        self.root_device.update_cpu_usage()
        self.system_monitor.record_cpu_usage(
            self.root_device.device_id, 
            self.root_device.current_cpu_usage,
            get_current_time(),
            'before_task'
        )
        
        # Make vertical load balancing decision
        decision = self.vertical_balancer.make_decision(task, balancing_condition)
        
        # Skip task if it's already missed deadline
        if decision == "skip":
            return None
            
        start_time = get_current_time()
        
        if decision == "edge":
            # If edge processing, decide on horizontal distribution
            if self.root_device.model:
                # Find computationally intensive layers that can be divided
                divisible_layers = [
                    (i, layer) for i, layer in enumerate(self.root_device.model.layers)
                    if layer.is_divisible and layer.is_computationally_intensive()
                ]
                
                # For now, simulate edge processing
                # In a full implementation, we would distribute layers across devices
                time.sleep(0.2)  # Simulate edge processing time
            
            result = self.root_device.execute_task(task)
            source = "edge"
        else:  # decision == "cloud"
            # Offload to cloud via server gateway
            result = self.server_gateway.send_to_cloud(task, self.root_device)
            source = "cloud"
            
        end_time = get_current_time()
        execution_time = end_time - start_time
        
        # Update task with results and metrics
        task.update_execution_results(result, execution_time, source)
        
        # Record CPU after task
        self.root_device.update_cpu_usage()
        self.system_monitor.record_cpu_usage(
            self.root_device.device_id, 
            self.root_device.current_cpu_usage,
            get_current_time(),
            'after_task'
        )
        
        # Record execution metrics
        deadline_missed = task.has_missed_deadline(end_time)
        self.system_monitor.record_execution(
            task.task_id,
            execution_time,
            source,
            deadline_missed
        )
        
        return result
        
    def process_queue(self, balancing_condition="cpu"):
       
        results = []
        while self.task_queue:
            task = self.task_queue.pop(0)
            result = self.process_task(task, balancing_condition)
            results.append(result)
        return results
        
    def run_experiment(self, num_tasks=100, balancing_condition="cpu"):
       
        # Clear previous data
        self.task_queue = []
        self.system_monitor = SystemMonitor()
        
        # Generate random tasks
        for i in range(num_tasks):
            # Random deadline between 0.5 and 10 seconds
            deadline = random.uniform(0.5, 10)
            
            # Random sensitivity (20% chance of being sensitive)
            is_sensitive = random.random() < 0.2
            
            self.create_task(deadline=deadline, is_sensitive=is_sensitive)
            
        # Process all tasks
        self.process_queue(balancing_condition)
        
        # Return experiment results
        return {
            'balancing_condition': balancing_condition,
            'num_tasks': num_tasks,
            'vertical_balancer_stats': self.vertical_balancer.get_statistics(),
            'system_stats': self.system_monitor.get_statistics()
        }
    
    def __repr__(self):
        return (f"LoadBalancingSystem(devices={len(self.root_device.connected_devices) + 1}, "
                f"queued_tasks={len(self.task_queue)})")