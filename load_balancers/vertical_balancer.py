class VerticalLoadBalancer:
    """Decides whether to process tasks at edge or cloud."""
    
    def __init__(self, root_device, server_gateway, cpu_threshold=33, deadline_threshold=7, 
                 task_count_threshold=25, decision_mode="weighted", weights=None, cloud_threshold=60):
        """
        Initialize vertical load balancer.
        
        Args:
            root_device: The root edge device
            server_gateway: The server gateway for cloud communication
            cpu_threshold (int): CPU utilization threshold percentage
            deadline_threshold (int): Task deadline threshold in seconds
            task_count_threshold (int): Number of edge tasks before cloud offloading
            decision_mode (str): Decision method ("cpu", "deadline", "count", or "weighted")
            weights (dict): Weights for different factors in weighted decision model
            cloud_threshold (int): Score threshold for cloud offloading (0-100)
        """
        self.root_device = root_device
        self.server_gateway = server_gateway
        self.cpu_threshold = cpu_threshold
        self.deadline_threshold = deadline_threshold
        self.task_count_threshold = task_count_threshold
        self.decision_mode = decision_mode
        self.weights = weights or {
            "cpu": 0.4,
            "deadline": 0.3,
            "computation": 0.2,
            "task_count": 0.1
        }
        self.cloud_threshold = cloud_threshold
        self.edge_task_counter = 0
        self.total_decisions = {
            "edge": 0,
            "cloud": 0,
            "skip": 0
        }
    
    def make_decision(self, task, balancing_condition=None):
        """
        Decide whether to offload task to cloud or process at edge.
        
        Args:
            task: The task to be processed
            balancing_condition: Legacy parameter to specify decision method
            
        Returns:
            str: Decision ("edge", "cloud", or "skip")
        """
        # Use specified balancing_condition if provided, otherwise use configured decision_mode
        decision_method = balancing_condition or self.decision_mode
        
        # Always process sensitive data at edge
        if task.is_sensitive:
            decision = "edge"
            self.total_decisions["edge"] += 1
            return decision
            
        # Skip tasks that have already missed their deadline
        current_time = get_current_time()
        if task.has_missed_deadline(current_time):
            decision = "skip"
            self.total_decisions["skip"] += 1
            return decision
        
        # Apply selected decision method
        if decision_method == "weighted":
            decision = self._make_weighted_decision(task, current_time)
        elif decision_method == "cpu":
            self.root_device.update_cpu_usage()
            if self.root_device.current_cpu_usage > self.cpu_threshold:
                decision = "cloud"
            else:
                decision = "edge"
        elif decision_method == "deadline":
            if task.deadline and task.deadline > self.deadline_threshold:
                decision = "cloud"
            else:
                decision = "edge"
        elif decision_method == "count":
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
    
    def _make_weighted_decision(self, task, current_time):
        """
        Make a decision based on weighted factors.
        
        Args:
            task: The task to be processed
            current_time: Current timestamp
            
        Returns:
            str: Decision ("edge" or "cloud")
        """
        score = 0
        
        # Factor 1: CPU utilization (0-100 points)
        self.root_device.update_cpu_usage()
        cpu_usage = self.root_device.current_cpu_usage
        cpu_score = min(100, cpu_usage * 1.5)  # Scale to give more weight
        score += cpu_score * self.weights["cpu"]
        
        # Factor 2: Task deadline (0-100 points)
        if task.deadline:
            # Shorter deadlines = higher score (need to process at edge)
            # Convert deadline to a 0-100 scale (10s deadline = 0, 0.5s deadline = 100)
            deadline_score = max(0, min(100, 100 * (1 - (task.deadline - 0.5) / 9.5)))
            score += deadline_score * self.weights["deadline"]
        
        # Factor 3: Task computational needs (0-100 points)
        # Use model layer count as proxy for computational needs
        if self.root_device.model:
            model_size = len(self.root_device.model.layers)
            # Larger models more likely to benefit from cloud offloading
            comp_score = min(100, model_size * 5)  # Scale based on typical model sizes
            score += comp_score * self.weights["computation"]
            
        # Factor 4: Recent edge execution count (0-100 points)
        # Balance workload by occasionally offloading
        count_score = min(100, (self.edge_task_counter / self.task_count_threshold) * 100)
        score += count_score * self.weights["task_count"]
        
        # Decision threshold
        if score >= self.cloud_threshold:  # Score above threshold suggests cloud offloading
            decision = "cloud"
            self.edge_task_counter = 0
        else:
            decision = "edge"
            self.edge_task_counter += 1
        
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
        return (f"VerticalLoadBalancer(mode={self.decision_mode}, "
                f"cpu_threshold={self.cpu_threshold}, "
                f"deadline_threshold={self.deadline_threshold}, "
                f"task_count_threshold={self.task_count_threshold})")
def record_decision_quality(self, task, decision, execution_time, deadline_missed):
    """Record metrics about decision quality."""
    if not hasattr(self, 'decision_metrics'):
        self.decision_metrics = {
            'edge': {'count': 0, 'missed_deadlines': 0, 'avg_execution': 0},
            'cloud': {'count': 0, 'missed_deadlines': 0, 'avg_execution': 0}
        }
    
    metrics = self.decision_metrics[decision]
    metrics['count'] += 1
    
    # Update running average of execution time
    metrics['avg_execution'] = ((metrics['avg_execution'] * (metrics['count'] - 1)) + 
                                execution_time) / metrics['count']
    
    if deadline_missed:
        metrics['missed_deadlines'] += 1

def get_decision_quality_metrics(self):
    """Get metrics about decision quality."""
    if not hasattr(self, 'decision_metrics'):
        return {'no_metrics_available': True}
    
    metrics = self.decision_metrics.copy()
    for location, data in metrics.items():
        if data['count'] > 0:
            data['deadline_miss_rate'] = (data['missed_deadlines'] / data['count']) * 100
        else:
            data['deadline_miss_rate'] = 0
    
    return metrics