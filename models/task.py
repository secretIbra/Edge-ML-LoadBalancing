import time

class Task:
    
    def __init__(self, task_id, input_data, deadline=None, is_sensitive=False):
      
        self.task_id = task_id
        self.input_data = input_data
        self.creation_time = time.time()
        self.deadline = deadline  # Seconds from creation
        self.is_sensitive = is_sensitive
        self.execution_time = None
        self.result = None
        self.source = None  # 'edge' or 'cloud'
        
    def has_missed_deadline(self, current_time=None):
        if self.deadline is None:
            return False
            
        current_time = current_time or time.time()
        return current_time > (self.creation_time + self.deadline)
    
    def get_remaining_time(self, current_time=None):
        if self.deadline is None:
            return None
            
        current_time = current_time or time.time()
        return (self.creation_time + self.deadline) - current_time
    
    def update_execution_results(self, result, execution_time, source):
        self.result = result
        self.execution_time = execution_time
        self.source = source
    
    def __repr__(self):
        status = "completed" if self.result else "pending"
        sensitive = "sensitive" if self.is_sensitive else "non-sensitive"
        return f"Task(id={self.task_id}, status={status}, {sensitive})"