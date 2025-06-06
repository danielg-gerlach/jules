import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any # Added Optional, List, Dict, Any for precise type hinting

# Define valid priority levels as a constant for easier maintenance and validation
VALID_PRIORITIES = ["High", "Medium", "Low"]


class Task:
    """
    Represents a single task with its attributes and methods for serialization.

    Attributes:
        id (str): Auto-generated unique identifier for the task.
        title (str): The title or name of the task.
        description (str): A more detailed description of the task.
        priority (str): The priority level of the task (e.g., "High", "Medium", "Low").
        due_date (str): The date when the task is due, in "YYYY-MM-DD" format.
        completed (bool): The completion status of the task, True if completed, False otherwise.
    """

    def __init__(self, title: str, description: str, priority: str, due_date: str,
                 completed: bool = False, id: Optional[str] = None):
        """
        Initializes a new Task object.

        Args:
            title: The title of the task.
            description: The detailed description of the task.
            priority: The priority level of the task. Must be one of VALID_PRIORITIES.
            due_date: The due date for the task, expected in "YYYY-MM-DD" format.
            completed: The completion status of the task. Defaults to False.
            id: Optional. The unique ID of the task. If None, a new UUID is generated.
        """
        self.id: str = id if id else uuid.uuid4().hex
        self.title: str = title
        self.description: str = description
        self.priority: str = priority
        self.due_date: str = due_date
        self.completed: bool = completed

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the Task object to a dictionary for storage or transmission.

        Returns:
            A dictionary representation of the task.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Creates a Task object from a dictionary representation.

        Args:
            data: A dictionary containing the task's attributes.

        Returns:
            A new Task instance.
        """
        return cls(
            id=data.get("id"),
            title=data.get("title", ""), # Provide default for robustness
            description=data.get("description", ""), # Provide default
            priority=data.get("priority", "Medium"), # Default priority
            due_date=data.get("due_date"),
            completed=data.get("completed", False)
        )

    def __repr__(self) -> str:
        """
        Returns an unambiguous string representation of the Task object, useful for debugging.
        """
        return (f"Task(id='{self.id}', title='{self.title}', priority='{self.priority}', "
                f"due_date='{self.due_date}', completed={self.completed})")


class TaskManager:
    """
    Manages a collection of tasks, including loading, saving, and CRUD operations.

    Attributes:
        filepath (str): The path to the JSON file used for storing tasks.
        tasks (List[Task]): A list of Task objects currently managed.
    """

    def __init__(self, filepath: str = 'tasks.json'):
        """
        Initializes the TaskManager.

        Args:
            filepath: The path to the JSON file for storing tasks. Defaults to 'tasks.json'.
                      The TaskManager will attempt to load tasks from this file.
        """
        self.filepath: str = filepath
        self.tasks: List[Task] = []
        self._load_tasks()

    def _validate_due_date(self, due_date: str) -> None:
        """Helper method to validate the due_date format."""
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format.")

    def _validate_priority(self, priority: str) -> None:
        """Helper method to validate the priority value."""
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {', '.join(VALID_PRIORITIES)}.")

    def _load_tasks(self) -> None:
        """
        Loads tasks from the JSON file specified by `self.filepath`.
        If the file is not found, the task list remains empty.
        If the file contains invalid JSON, an error message is printed, and the list remains empty.
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f: # Specify encoding
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            self.tasks = []  # Start with an empty list if no file exists
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.filepath}. Starting with an empty task list.")
            self.tasks = []
        except Exception as e: # Catch other potential errors during loading
            print(f"An unexpected error occurred while loading tasks: {e}")
            self.tasks = []


    def _save_tasks(self) -> None:
        """
        Saves the current list of tasks to the JSON file specified by `self.filepath`.
        Tasks are serialized to dictionaries before being written as JSON.
        """
        try:
            with open(self.filepath, 'w', encoding='utf-f') as f: # Specify encoding
                json.dump([task.to_dict() for task in self.tasks], f, indent=4, ensure_ascii=False)
        except IOError as e:
            # Log error or raise a custom exception to be handled by UI/caller
            print(f"Error saving tasks to {self.filepath}: {e}")
        except Exception as e: # Catch other potential errors during saving
            print(f"An unexpected error occurred while saving tasks: {e}")


    def add_task(self, title: str, description: str, priority: str, due_date: str) -> Task:
        """
        Creates a new task, adds it to the manager's list, and saves all tasks.

        Args:
            title: The title of the task.
            description: The detailed description of the task.
            priority: The priority level (e.g., "High", "Medium", "Low").
            due_date: The due date in "YYYY-MM-DD" format.

        Returns:
            The newly created Task object.

        Raises:
            ValueError: If `due_date` or `priority` are invalid.
        """
        self._validate_due_date(due_date)
        self._validate_priority(priority)

        new_task = Task(title=title, description=description,
                        priority=priority, due_date=due_date)
        self.tasks.append(new_task)
        self._save_tasks()
        return new_task

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieves a specific task by its unique ID.

        Args:
            task_id: The ID of the task to find.

        Returns:
            The Task object if found, otherwise None.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def edit_task(self, task_id: str, title: Optional[str] = None,
                  description: Optional[str] = None, priority: Optional[str] = None,
                  due_date: Optional[str] = None, completed: Optional[bool] = None) -> bool:
        """
        Edits attributes of an existing task identified by `task_id`.
        Only attributes for which a non-None value is provided are updated.

        Args:
            task_id: The ID of the task to be edited.
            title: Optional. The new title for the task.
            description: Optional. The new description for the task.
            priority: Optional. The new priority for the task.
            due_date: Optional. The new due date for the task (YYYY-MM-DD).
            completed: Optional. The new completion status for the task.

        Returns:
            True if the task was found and successfully edited, False otherwise.

        Raises:
            ValueError: If `due_date` or `priority` (if provided) are invalid.
        """
        task = self.get_task(task_id)
        if not task:
            return False

        changes_made = False
        if title is not None:
            task.title = title
            changes_made = True
        if description is not None:
            task.description = description
            changes_made = True
        if priority is not None:
            self._validate_priority(priority)
            task.priority = priority
            changes_made = True
        if due_date is not None:
            self._validate_due_date(due_date)
            task.due_date = due_date
            changes_made = True
        if completed is not None:
            task.completed = completed
            changes_made = True

        if changes_made:
            self._save_tasks()
        return True

    def delete_task(self, task_id: str) -> bool:
        """
        Deletes a task from the manager's list by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was found and deleted, False otherwise.
        """
        task_to_delete = self.get_task(task_id)
        if task_to_delete:
            self.tasks.remove(task_to_delete)
            self._save_tasks()
            return True
        return False

    def toggle_complete(self, task_id: str) -> bool:
        """
        Toggles the completion status of a task identified by its ID.

        Args:
            task_id: The ID of the task whose completion status is to be toggled.

        Returns:
            True if the task was found and its status toggled, False otherwise.
        """
        task = self.get_task(task_id)
        if task:
            task.completed = not task.completed
            self._save_tasks()
            return True
        return False

    def get_all_tasks(self) -> List[Task]:
        """
        Returns a shallow copy of the list of all tasks.
        Modifying the returned list will not affect the TaskManager's internal list,
        but modifying the Task objects within the list will affect them.

        Returns:
            A list of all Task objects.
        """
        return self.tasks[:]  # Return a copy

    def get_tasks_by_priority(self, priority_level: str) -> List[Task]:
        """
        Retrieves a list of tasks that match the specified priority level.

        Args:
            priority_level: The priority level to filter by.

        Returns:
            A list of tasks matching the criteria.

        Raises:
            ValueError: If `priority_level` is invalid.
        """
        self._validate_priority(priority_level)
        return [task for task in self.tasks if task.priority == priority_level]

    def get_tasks_by_completion(self, completed_status: bool) -> List[Task]:
        """
        Retrieves a list of tasks based on their completion status.

        Args:
            completed_status: True to get completed tasks, False for pending tasks.

        Returns:
            A list of tasks matching the criteria.
        """
        return [task for task in self.tasks if task.completed == completed_status]

    def clear_all_tasks(self) -> None:
        """
        Removes all tasks from the TaskManager and clears the storage file.
        This action is irreversible for the current session's data and the file.
        """
        self.tasks = []
        self._save_tasks()  # Writes an empty list to the file
