


# Vertical load balancer settings
VERTICAL_BALANCER = {
    "cpu_threshold": 33,         # CPU utilization percentage threshold
    "deadline_threshold": 7,     # Task deadline threshold in seconds
    "task_count_threshold": 25,  # Number of edge tasks before cloud offloading
    
    # New weighted model configuration
    "decision_mode": "weighted", # Options: "cpu", "deadline", "count", "weighted" 
    "weights": {
        "cpu": 0.4,              # Weight for CPU utilization (40%)
        "deadline": 0.3,         # Weight for task deadline (30%)
        "computation": 0.2,      # Weight for computational needs (20%)
        "task_count": 0.1        # Weight for recent edge execution count (10%)
    },
    "cloud_threshold": 60        # Score threshold for cloud offloading decision (0-100)
}

# Cloud connection settings
CLOUD = {
    "min_latency": 0.1,          # Minimum network latency in seconds
    "max_latency": 0.3,          # Maximum network latency in seconds
    "success_rate": 0.95         # Connection success probability
}

# Edge device configurations
EDGE_DEVICES = [
    {
        "device_id": "edge1",
        "cpu_speed": 1.2,        # GHz
        "num_cores": 4
    },
    {
        "device_id": "edge2",
        "cpu_speed": 2.4,        # GHz
        "num_cores": 4
    },
    {
        "device_id": "edge3",
        "cpu_speed": 1.0,        # GHz
        "num_cores": 2
    }
]

# Root device configuration
ROOT_DEVICE = {
    "device_id": "root",
    "cpu_speed": 1.4,            # GHz
    "num_cores": 4
}

# Task generation settings
TASK_GENERATION = {
    "min_deadline": 0.5,         # Minimum deadline in seconds
    "max_deadline": 10,          # Maximum deadline in seconds
    "sensitive_data_ratio": 0.2  # Ratio of tasks with sensitive data
}

# Around line 43-50 in config.py
EXPERIMENTS = {
    "num_tasks": 1000,           # Default number of tasks per experiment
    "conditions": [              # Load balancing conditions to test
        "cpu",
        "deadline",
        "count",
        "weighted"               # Add the new weighted condition here
    ]
}

# ML models configuration
MODELS = {
    "alexnet": {
        "name": "AlexNet",
        "conv_layers": 5,
        "linear_layers": 3
    },
    "vgg11": {
        "name": "VGG11",
        "conv_layers": 8,
        "linear_layers": 3
    },
    "vgg19": {
        "name": "VGG19",
        "conv_layers": 16,
        "linear_layers": 3
    }
}

# System monitoring settings
MONITORING = {
    "log_cpu_interval": 0.1,     # Interval in seconds for CPU logging
    "save_results": True,        # Whether to save results to file
    "results_file": "results.json"  # File to save results
}