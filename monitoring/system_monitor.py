
class SystemMonitor:
    
    def __init__(self):
        self.cpu_history = []
        self.execution_times = []
        self.missed_deadlines = 0
        self.total_tasks = 0
        
    def record_cpu_usage(self, device_id, cpu_usage, timestamp, state):
        self.cpu_history.append({
            'device_id': device_id,
            'cpu_usage': cpu_usage,
            'timestamp': timestamp,
            'state': state
        })
        
    def record_execution(self, task_id, execution_time, source, deadline_missed):
    
        self.execution_times.append({
            'task_id': task_id,
            'execution_time': execution_time,
            'source': source
        })
        
        self.total_tasks += 1
        if deadline_missed:
            self.missed_deadlines += 1
            
    def get_average_cpu_usage(self, device_id=None, state=None):
        filtered = self.cpu_history
        
        if device_id is not None:
            filtered = [entry for entry in filtered if entry['device_id'] == device_id]
            
        if state is not None:
            filtered = [entry for entry in filtered if entry['state'] == state]
            
        if not filtered:
            return 0
            
        return sum(entry['cpu_usage'] for entry in filtered) / len(filtered)
        
    def get_average_execution_time(self, source=None):
       
        filtered = self.execution_times
        
        if source is not None:
            filtered = [entry for entry in filtered if entry['source'] == source]
            
        if not filtered:
            return 0
            
        return sum(entry['execution_time'] for entry in filtered) / len(filtered)
    
    def get_deadline_miss_rate(self):
       
        if self.total_tasks == 0:
            return 0
        return (self.missed_deadlines / self.total_tasks) * 100
    
    def get_statistics(self):
       
        return {
            'cpu_usage': {
                'overall': self.get_average_cpu_usage(),
                'before_task': self.get_average_cpu_usage(state='before_task'),
                'after_task': self.get_average_cpu_usage(state='after_task')
            },
            'execution_time': {
                'overall': self.get_average_execution_time(),
                'edge': self.get_average_execution_time(source='edge'),
                'cloud': self.get_average_execution_time(source='cloud')
            },
            'deadline_performance': {
                'total_tasks': self.total_tasks,
                'missed_deadlines': self.missed_deadlines,
                'miss_rate': self.get_deadline_miss_rate()
            }
        }
    
    def __repr__(self):
        return f"SystemMonitor(tasks={self.total_tasks}, missed_deadlines={self.missed_deadlines})"