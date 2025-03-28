

from utils.helpers import get_current_time

class VerticalLoadBalancer:
    """Decides whether to process tasks at edge or cloud."""
    
    def __init__(self, root_device, server_gateway, cpu_threshold=33, deadline_threshold=7, task_count_threshold=25):
        """
        Initialize vertical load balancer.
        
        Args:
            root_device: The root edge device
            server_gateway: The server gateway for cloud communication
            cpu_threshold (int): CPU utilization threshold percentage
            deadline_threshold (int): Task deadline threshold in seconds
            task_count_threshold (int): Number of edge tasks before cloud offloading
        """
        self.root_device = root_device
        self.server_gateway = server_gateway
        self.cpu_threshold = cpu_threshold
        self.deadline_threshold = deadline_threshold
        self.task_count_threshold = task_count_threshold
        self.edge_task_counter = 0
        self.total_decisions = {
            "edge": 0,
            "cloud": 0,
            "skip": 0
        }
    
    def make_decision(self, task, balancing_condition="cpu"):
        """
        Decide whether to offload task to cloud or process at edge.
        
        """
        # Always process sensitive data at edge
        if task.is_sensitive:
            decision = "edge"
            self.total_decisions["edge"] += 1
            return decision
            
        # Skip tasks that have already missed their deadline
        if task.has_missed_deadline(get_current_time()):
            decision = "skip"
            self.total_decisions["skip"] += 1
            return decision
        
        # Apply selected balancing condition
        if balancing_condition == "cpu":
            self.root_device.update_cpu_usage()
            if self.root_device.current_cpu_usage > self.cpu_threshold:
                decision = "cloud"
            else:
                decision = "edge"
                
        elif balancing_condition == "deadline":
            if task.deadline and task.deadline > self.deadline_threshold:
                decision = "cloud"
            else:
                decision = "edge"
                
        elif balancing_condition == "count":
            self.edge_task_counter += 1
            if self.edge_task_counter >= self.task_count_threshold:
                self.edge_task_counter = 0
                decision = "cloud"
            else:
                decision = "edge"
        else:
            # Default to edge processing
            decision = "edge"
        
        self.total_decisions[decision] += 1
        return decision
    
    def get_statistics(self):
        total = sum(self.total_decisions.values())
        if total == 0:
            return {k: 0 for k in self.total_decisions}
            
        return {
            k: {
                "count": v,
                "percentage": (v / total) * 100
            }
            for k, v in self.total_decisions.items()
        }
    
    def __repr__(self):
        return (f"VerticalLoadBalancer(cpu_threshold={self.cpu_threshold}, "
                f"deadline_threshold={self.deadline_threshold}, "
                f"task_count_threshold={self.task_count_threshold})")