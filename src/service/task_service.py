from src.repository.task_repository import TaskRepository

class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository