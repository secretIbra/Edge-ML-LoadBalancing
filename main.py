
import argparse
import time
import json
from load_balancing_system import LoadBalancingSystem
from utils.helpers import save_results, create_alexnet_model, create_vgg11_model
import config

def setup_system():
    # Create system
    system = LoadBalancingSystem()
    
    # Configure root device from config
    system.root_device.cpu_speed = config.ROOT_DEVICE["cpu_speed"]
    system.root_device.num_cores = config.ROOT_DEVICE["num_cores"]
    
    # Add edge devices from config
    for device_config in config.EDGE_DEVICES:
        system.add_edge_device(
            device_config["device_id"],
            device_config["cpu_speed"],
            device_config["num_cores"]
        )
    
    # Configure cloud service
    system.cloud_service.latency_range = (
        config.CLOUD["min_latency"],
        config.CLOUD["max_latency"]
    )
    system.cloud_service.success_rate = config.CLOUD["success_rate"]
    
    # Configure vertical load balancer
    system.vertical_balancer.cpu_threshold = config.VERTICAL_BALANCER["cpu_threshold"]
    system.vertical_balancer.deadline_threshold = config.VERTICAL_BALANCER["deadline_threshold"]
    system.vertical_balancer.task_count_threshold = config.VERTICAL_BALANCER["task_count_threshold"]
    
    return system

def run_experiments(model_name="alexnet"):

    # Set up system
    system = setup_system()
    
    # Load model based on name
    if model_name.lower() == "alexnet":
        model = create_alexnet_model()
    elif model_name.lower() == "vgg11":
        model = create_vgg11_model()
    else:
        raise ValueError(f"Unknown model: {model_name}")
        
    system.load_model(model)
    
    # Run experiments with different conditions
    results = {}
    for condition in config.EXPERIMENTS["conditions"]:
        print(f"Running experiment with {model_name} using {condition} condition...")
        start_time = time.time()
        
        experiment_result = system.run_experiment(
            num_tasks=config.EXPERIMENTS["num_tasks"],
            balancing_condition=condition
        )
        
        end_time = time.time()
        experiment_result["duration"] = end_time - start_time
        
        results[condition] = experiment_result
        
        print(f"  - Completed in {experiment_result['duration']:.2f} seconds")
        print(f"  - Missed deadlines: {experiment_result['system_stats']['deadline_performance']['missed_deadlines']}")
        print(f"  - Avg CPU before tasks: {experiment_result['system_stats']['cpu_usage']['before_task']:.2f}%")
        print(f"  - Avg CPU after tasks: {experiment_result['system_stats']['cpu_usage']['after_task']:.2f}%")
        print()
    
    # Combine results
    combined_results = {
        "model": model_name,
        "timestamp": time.time(),
        "experiments": results
    }
    
    # Save results if configured
    if config.MONITORING["save_results"]:
        save_results(combined_results, config.MONITORING["results_file"])
    
    return combined_results

def main():
    """Main entry point for the system."""
    parser = argparse.ArgumentParser(description="Online Horizontal & Vertical Edge ML Load Balancing System")
    parser.add_argument("--model", type=str, default="alexnet", choices=["alexnet", "vgg11"],
                        help="ML model to use for experiments")
    parser.add_argument("--tasks", type=int, default=config.EXPERIMENTS["num_tasks"],
                        help="Number of tasks to generate")
    parser.add_argument("--condition", type=str, choices=["cpu", "deadline", "count", "all"],
                        default="all", help="Load balancing condition to test")
    
    args = parser.parse_args()
    
    # Update config based on arguments
    config.EXPERIMENTS["num_tasks"] = args.tasks
    
    if args.condition != "all":
        config.EXPERIMENTS["conditions"] = [args.condition]
    
    # Run experiments
    results = run_experiments(args.model)
    
    # Print summary
    print("\nExperiment Summary:")
    print(f"Model: {results['model']}")
    print(f"Total tasks: {args.tasks}")
    
    for condition, result in results["experiments"].items():
        print(f"\nCondition: {condition}")
        print(f"  Cloud tasks: {result['vertical_balancer_stats']['cloud']['count']}")
        print(f"  Edge tasks: {result['vertical_balancer_stats']['edge']['count']}")
        print(f"  Skipped tasks: {result['vertical_balancer_stats']['skip']['count']}")
        print(f"  Missed deadlines: {result['system_stats']['deadline_performance']['missed_deadlines']}")
        print(f"  Miss rate: {result['system_stats']['deadline_performance']['miss_rate']:.2f}%")
        print(f"  Avg execution time (edge): {result['system_stats']['execution_time']['edge']:.4f}s")
        print(f"  Avg execution time (cloud): {result['system_stats']['execution_time']['cloud']:.4f}s")

if __name__ == "__main__":
    main()