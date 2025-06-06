import tkinter as tk
from tkinter import ttk, messagebox
# Assuming task_manager.py is in the same directory
from task_manager import TaskManager, Task, VALID_PRIORITIES
from datetime import datetime
from typing import Optional, List, Any # Added Optional, List, Any

# Imports for Matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

# Constants for filter options
FILTER_PRIORITY_OPTIONS = ["All"] + VALID_PRIORITIES
FILTER_STATUS_OPTIONS = ["All", "Pending", "Completed"]


class StatsWindow(tk.Toplevel):
    """
    A dialog window for displaying task statistics and charts.
    Provides visual insights into task distribution by priority and completion status.
    """

    def __init__(self, parent: tk.Tk, task_manager: TaskManager):
        """
        Initializes the StatsWindow.

        Args:
            parent: The parent window (MainApplication instance).
            task_manager: The TaskManager instance for accessing task data.
        """
        super().__init__(parent)
        self.parent = parent
        self.task_manager = task_manager

        self.title("Task Statistics")
        self.geometry("700x750")
        self.resizable(True, True)
        self.transient(parent)  # Ensure dialog stays on top of the parent window
        self.grab_set()  # Make the dialog modal

        tasks: List[Task] = self.task_manager.get_all_tasks()

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._display_summary_stats(tasks, main_frame)

        charts_frame = ttk.Frame(main_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self._display_priority_chart(tasks, charts_frame)
        self._display_completion_chart(tasks, charts_frame)

    def _display_summary_stats(self, tasks: List[Task], parent_frame: ttk.Frame) -> None:
        """
        Displays textual summary statistics of tasks.

        Args:
            tasks: A list of Task objects to summarize.
            parent_frame: The parent ttk.Frame in which to place these stats.
        """
        summary_frame = ttk.LabelFrame(
            parent_frame, text="Summary Statistics", padding="10")
        summary_frame.pack(fill=tk.X, pady=5)

        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.completed)
        pending_tasks = total_tasks - completed_tasks

        ttk.Label(summary_frame, text=f"Total Tasks: {total_tasks}").pack(anchor="w")
        ttk.Label(summary_frame, text=f"Completed Tasks: {completed_tasks}").pack(anchor="w")
        ttk.Label(summary_frame, text=f"Pending Tasks: {pending_tasks}").pack(anchor="w")

        if not tasks:
            ttk.Label(summary_frame, text="No tasks available to generate detailed statistics.").pack(
                anchor="w", pady=5)

    def _display_priority_chart(self, tasks: List[Task], parent_frame: ttk.Frame) -> None:
        """
        Displays a bar chart showing the distribution of tasks by priority.

        Args:
            tasks: A list of Task objects.
            parent_frame: The parent ttk.Frame for the chart.
        """
        priority_frame = ttk.LabelFrame(parent_frame, text="Task Priorities", padding="10")
        priority_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        if not tasks:
            ttk.Label(priority_frame, text="No data to display.").pack(padx=10, pady=10)
            return

        priority_counts = Counter(task.priority for task in tasks)
        # Use VALID_PRIORITIES to ensure consistent order and inclusion of all levels
        counts = [priority_counts.get(p, 0) for p in VALID_PRIORITIES]

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        colors = {'Low': '#4CAF50', 'Medium': '#FFC107', 'High': '#F44336'}
        bar_colors = [colors.get(p, '#CCCCCC') for p in VALID_PRIORITIES] # Default color for safety

        bars = ax.bar(VALID_PRIORITIES, counts, color=bar_colors)
        ax.set_title("Distribution by Priority")
        ax.set_ylabel("Number of Tasks")
        ax.set_xlabel("Priority Level")

        # Add counts on top of bars for clarity
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.05, int(yval), ha='center', va='bottom')

        fig.tight_layout()  # Adjust layout to prevent labels from overlapping

        canvas = FigureCanvasTkAgg(fig, master=priority_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    def _display_completion_chart(self, tasks: List[Task], parent_frame: ttk.Frame) -> None:
        """
        Displays a pie chart showing the proportion of completed vs. pending tasks.

        Args:
            tasks: A list of Task objects.
            parent_frame: The parent ttk.Frame for the chart.
        """
        completion_frame = ttk.LabelFrame(parent_frame, text="Task Completion Status", padding="10")
        completion_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        if not tasks:
            ttk.Label(completion_frame, text="No data to display.").pack(padx=10, pady=10)
            return

        completed_count = sum(1 for task in tasks if task.completed)
        pending_count = len(tasks) - completed_count

        if completed_count == 0 and pending_count == 0:
            ttk.Label(completion_frame, text="No tasks with completion status.").pack(padx=10, pady=10)
            return

        labels = 'Completed', 'Pending'
        sizes = [completed_count, pending_count]
        colors = ['#4CAF50', '#FF9800']  # Green for completed, Orange for pending
        explode = (0.1, 0) if completed_count > 0 and pending_count > 0 else (0, 0)  # Explode if both slices exist

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.axis('equal')  # Ensures pie is drawn as a circle.
        ax.set_title("Completion Status")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=completion_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()


class TaskDialog(tk.Toplevel):
    """
    A modal dialog window for adding a new task or editing an existing one.
    """

    def __init__(self, parent: tk.Tk, task_manager: TaskManager, task_data: Optional[Task] = None):
        """
        Initializes the TaskDialog.

        Args:
            parent: The parent window (MainApplication instance).
            task_manager: The TaskManager instance for data operations.
            task_data: Optional. The Task object to edit. If None, the dialog is for adding a new task.
        """
        super().__init__(parent)
        self.parent = parent  # Store parent for callbacks (e.g., refreshing list)
        self.task_manager = task_manager
        self.task_data = task_data  # None if adding, Task object if editing

        self.title("Edit Task" if self.task_data else "Add Task")
        self.geometry("400x450")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()  # Make dialog modal

        self._create_widgets()
        if self.task_data:
            self._populate_fields()

        self.protocol("WM_DELETE_WINDOW", self.destroy) # Ensure grab_release on close

    def _create_widgets(self) -> None:
        """Creates and lays out the input fields and buttons in the dialog."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(main_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = ttk.Entry(main_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Description
        ttk.Label(main_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.description_text = tk.Text(main_frame, width=30, height=8, wrap=tk.WORD)
        desc_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.description_text.yview)
        self.description_text.configure(yscrollcommand=desc_scrollbar.set)
        self.description_text.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        desc_scrollbar.grid(row=1, column=2, padx=(0, 5), pady=5, sticky="ns")

        # Priority
        ttk.Label(main_frame, text="Priority:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.priority_combobox = ttk.Combobox(main_frame, values=VALID_PRIORITIES, state="readonly")
        self.priority_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.priority_combobox.set("Medium")  # Default priority

        # Due Date
        ttk.Label(main_frame, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.due_date_entry = ttk.Entry(main_frame, width=40)
        self.due_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        # Set initial date, today for new tasks, existing for edited tasks
        initial_date = self.task_data.due_date if self.task_data and self.task_data.due_date else datetime.now().strftime("%Y-%m-%d")
        self.due_date_entry.insert(0, initial_date)

        # Completed Checkbox (only shown when editing an existing task)
        if self.task_data:
            self.completed_var = tk.BooleanVar(value=self.task_data.completed)
            ttk.Checkbutton(main_frame, text="Completed", variable=self.completed_var).grid(
                row=4, column=1, padx=5, pady=10, sticky="w"
            )

        # Buttons Frame for Save and Cancel
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=15, sticky="e")

        self.save_button = ttk.Button(button_frame, text="Save", command=self._save_task)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        main_frame.columnconfigure(1, weight=1)  # Allow input fields to expand horizontally

    def _populate_fields(self) -> None:
        """Populates input fields with existing task data if editing."""
        if self.task_data:
            self.title_entry.insert(0, self.task_data.title)
            self.description_text.insert(tk.END, self.task_data.description)
            self.priority_combobox.set(self.task_data.priority)
            # Due date is pre-filled by _create_widgets logic
            # self.completed_var is initialized directly in _create_widgets

    def _validate_inputs(self) -> bool:
        """
        Validates the user-entered data in the input fields.
        Shows error message boxes for invalid inputs.

        Returns:
            True if all inputs are valid, False otherwise.
        """
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Validation Error", "Title cannot be empty.", parent=self)
            return False

        due_date_str = self.due_date_entry.get().strip()
        try:
            datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation Error", "Due date must be in YYYY-MM-DD format.", parent=self)
            return False

        priority = self.priority_combobox.get()
        if not priority: # Should not happen with "readonly" state and default
            messagebox.showerror("Validation Error", "Please select a priority.", parent=self)
            return False
        if priority not in VALID_PRIORITIES: # Defensive check
            messagebox.showerror("Validation Error", f"Invalid priority. Choose from {', '.join(VALID_PRIORITIES)}.", parent=self)
            return False

        return True

    def _save_task(self) -> None:
        """
        Handles the save operation. Validates inputs, then either adds a new task
        or edits an existing one through the TaskManager.
        Refreshes the parent's task list and closes the dialog on success.
        """
        if not self._validate_inputs():
            return  # Stop if validation fails

        title = self.title_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        priority = self.priority_combobox.get()
        due_date = self.due_date_entry.get().strip()

        try:
            if self.task_data:  # Editing existing task
                completed_status = self.completed_var.get() if hasattr(self, 'completed_var') else self.task_data.completed
                self.task_manager.edit_task(
                    task_id=self.task_data.id,
                    title=title,
                    description=description,
                    priority=priority,
                    due_date=due_date,
                    completed=completed_status
                )
                self.parent._update_status_bar(f"Task '{title}' updated.")
            else:  # Adding new task
                self.task_manager.add_task(
                    title=title,
                    description=description,
                    priority=priority,
                    due_date=due_date
                )
                self.parent._update_status_bar(f"Task '{title}' added.")

            self.parent._refresh_task_list()  # Update the list in the main application
            self.destroy()  # Close the dialog
        except ValueError as e: # Catch validation errors from TaskManager (e.g. bad priority string if not using combobox)
            messagebox.showerror("Save Error", str(e), parent=self)
        except Exception as e: # Catch unexpected errors
            messagebox.showerror("Save Error", f"An unexpected error occurred: {e}", parent=self)


class MainApplication(tk.Tk):
    """
    The main application window for the Task Manager.
    Manages the display of tasks, user interactions, and control elements.
    """

    def __init__(self, task_manager_instance: TaskManager):
        """
        Initializes the MainApplication.

        Args:
            task_manager_instance: An instance of the TaskManager for backend operations.
        """
        super().__init__()
        self.task_manager = task_manager_instance

        self.title("TkTask - Task Manager")
        self.geometry("850x600") # Slightly wider for the stats button

        self._create_control_widgets()
        self._create_task_list_widgets()
        self._create_status_bar()

        self._refresh_task_list()
        self._update_button_states()

    def _create_control_widgets(self) -> None:
        """Creates and places the control buttons and filter widgets."""
        controls_frame = ttk.Frame(self, padding="10")
        controls_frame.pack(fill=tk.X)

        # --- Buttons Sub-frame ---
        button_sub_frame = ttk.Frame(controls_frame)
        button_sub_frame.pack(side=tk.LEFT, padx=(0, 10)) # Reduced right padding

        self.add_button = ttk.Button(button_sub_frame, text="Add Task", command=self._open_add_task_dialog)
        self.add_button.grid(row=0, column=0, padx=2, pady=5) # Reduced padx

        self.edit_button = ttk.Button(button_sub_frame, text="Edit Selected", command=self._open_edit_task_dialog)
        self.edit_button.grid(row=0, column=1, padx=2, pady=5)

        self.delete_button = ttk.Button(button_sub_frame, text="Delete Selected", command=self._delete_selected_task)
        self.delete_button.grid(row=0, column=2, padx=2, pady=5)

        self.toggle_button = ttk.Button(button_sub_frame, text="Toggle Complete", command=self._toggle_selected_task_completion)
        self.toggle_button.grid(row=0, column=3, padx=2, pady=5)

        self.stats_button = ttk.Button(button_sub_frame, text="View Statistics", command=self._open_stats_window)
        self.stats_button.grid(row=0, column=4, padx=(2,0), pady=5) # No right padx for last button

        # --- Filters Sub-frame ---
        filter_sub_frame = ttk.Frame(controls_frame)
        filter_sub_frame.pack(side=tk.LEFT, padx=(10, 0)) # Reduced left padding

        ttk.Label(filter_sub_frame, text="Priority:").grid(row=0, column=0, padx=(0,2), pady=5, sticky="w")
        self.priority_filter_var = tk.StringVar(value="All")
        self.priority_filter_combo = ttk.Combobox(
            filter_sub_frame, textvariable=self.priority_filter_var,
            values=FILTER_PRIORITY_OPTIONS, state="readonly", width=10
        )
        self.priority_filter_combo.grid(row=0, column=1, padx=2, pady=5)
        self.priority_filter_combo.bind("<<ComboboxSelected>>", self._filter_tasks)

        ttk.Label(filter_sub_frame, text="Status:").grid(row=0, column=2, padx=(5,2), pady=5, sticky="w") # Added left padding
        self.status_filter_var = tk.StringVar(value="All")
        self.status_filter_combo = ttk.Combobox(
            filter_sub_frame, textvariable=self.status_filter_var,
            values=FILTER_STATUS_OPTIONS, state="readonly", width=10
        )
        self.status_filter_combo.grid(row=0, column=3, padx=2, pady=5)
        self.status_filter_combo.bind("<<ComboboxSelected>>", self._filter_tasks)

    def _create_task_list_widgets(self) -> None:
        """Creates the Treeview widget for displaying tasks along with its scrollbar."""
        task_list_frame = ttk.Frame(self, padding=(10, 0, 10, 10))
        task_list_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "title", "priority", "due_date", "status")
        self.task_tree = ttk.Treeview(task_list_frame, columns=columns, show="headings", selectmode="browse")

        # Define column headings
        self.task_tree.heading("id", text="ID")
        self.task_tree.heading("title", text="Title")
        self.task_tree.heading("priority", text="Priority")
        self.task_tree.heading("due_date", text="Due Date")
        self.task_tree.heading("status", text="Status")

        # Configure column properties
        self.task_tree.column("id", width=0, stretch=tk.NO)  # Hidden: Used internally for ID retrieval
        self.task_tree.column("title", width=300, anchor="w") # Increased width for title
        self.task_tree.column("priority", width=100, anchor="center")
        self.task_tree.column("due_date", width=120, anchor="center")
        self.task_tree.column("status", width=100, anchor="center")

        # Scrollbar
        tree_scrollbar = ttk.Scrollbar(task_list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.task_tree.grid(row=0, column=0, sticky="nsew")
        tree_scrollbar.grid(row=0, column=1, sticky="ns")

        # Make the Treeview expandable
        task_list_frame.grid_rowconfigure(0, weight=1)
        task_list_frame.grid_columnconfigure(0, weight=1)

        # Event bindings
        self.task_tree.bind("<Double-1>", lambda event: self._open_edit_task_dialog()) # event arg is conventional
        self.task_tree.bind("<<TreeviewSelect>>", self._on_task_select)

    def _create_status_bar(self) -> None:
        """Creates a status bar at the bottom of the window for messages."""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w", padding=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _update_status_bar(self, message: str) -> None:
        """Updates the text displayed in the status bar."""
        self.status_var.set(message)

    def _refresh_task_list(self, tasks_to_display: Optional[List[Task]] = None) -> None:
        """
        Clears and repopulates the task list Treeview.
        Tasks are sorted by due date (ascending) then by priority (High, Medium, Low).

        Args:
            tasks_to_display: Optional. A specific list of tasks to display.
                              If None, all tasks from TaskManager are fetched.
        """
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        tasks = tasks_to_display if tasks_to_display is not None else self.task_manager.get_all_tasks()

        # Sort tasks: Primary key due_date (chronological), Secondary key priority (High=0, Medium=1, Low=2)
        priority_map = {p: i for i, p in enumerate(VALID_PRIORITIES)} # High=0, Medium=1, Low=2
        try:
            tasks.sort(key=lambda t: (datetime.strptime(t.due_date, "%Y-%m-%d"), priority_map.get(t.priority, len(VALID_PRIORITIES))))
        except ValueError as e: # Handle potential malformed due dates if TaskManager validation was bypassed
            print(f"Warning: Error sorting tasks by due date - {e}. Some dates might be malformed.")
            tasks.sort(key=lambda t: priority_map.get(t.priority, len(VALID_PRIORITIES))) # Fallback sort by priority

        for task in tasks:
            status_str = "Completed" if task.completed else "Pending"
            self.task_tree.insert("", tk.END, values=(task.id, task.title, task.priority, task.due_date, status_str))

        self._update_button_states()

    def _filter_tasks(self, event: Optional[Any] = None) -> None: # event is passed by bind, can be None
        """
        Filters tasks based on selected criteria in priority and status comboboxes,
        then refreshes the task list.
        """
        priority_filter = self.priority_filter_var.get()
        status_filter = self.status_filter_var.get()

        # Start with all tasks and apply filters sequentially
        current_tasks = self.task_manager.get_all_tasks()

        if priority_filter != "All":
            current_tasks = [task for task in current_tasks if task.priority == priority_filter]

        if status_filter != "All":
            status_bool = (status_filter == "Completed")
            current_tasks = [task for task in current_tasks if task.completed == status_bool]

        self._refresh_task_list(tasks_to_display=current_tasks)
        self._update_status_bar(f"Filtered view: Priority '{priority_filter}', Status '{status_filter}'.")

    def _get_selected_task_id(self) -> Optional[str]:
        """
        Retrieves the ID of the currently selected task in the Treeview.
        The ID is stored as the first value in the Treeview item's `values` tuple.

        Returns:
            The ID of the selected task as a string, or None if no task is selected.
        """
        selected_item_iid = self.task_tree.focus()  # Gets the IID (internal ID) of the focused item
        if selected_item_iid:
            item_values = self.task_tree.item(selected_item_iid, "values")
            if item_values and isinstance(item_values, (list, tuple)) and len(item_values) > 0:
                return str(item_values[0]) # Ensure it's a string
        return None

    def _open_add_task_dialog(self) -> None:
        """Opens the TaskDialog for adding a new task."""
        TaskDialog(self, self.task_manager) # Dialog handles its lifecycle and parent updates

    def _open_edit_task_dialog(self, event: Optional[Any] = None) -> None: # event from double-click
        """Opens the TaskDialog to edit the currently selected task."""
        selected_task_id = self._get_selected_task_id()
        if not selected_task_id:
            messagebox.showerror("Error", "No task selected. Please select a task to edit.", parent=self)
            return

        task_object = self.task_manager.get_task(selected_task_id)
        if task_object:
            TaskDialog(self, self.task_manager, task_data=task_object)
        else: # Should ideally not happen if list is in sync with backend
            messagebox.showerror("Error", "Could not find the selected task. It might have been deleted.", parent=self)
            self._refresh_task_list()

    def _delete_selected_task(self) -> None:
        """Deletes the selected task from the TaskManager after user confirmation."""
        selected_task_id = self._get_selected_task_id()
        if not selected_task_id:
            messagebox.showerror("Error", "No task selected. Please select a task to delete.", parent=self)
            return

        task = self.task_manager.get_task(selected_task_id) # Get task details for confirmation message
        if not task: # Should not happen
            messagebox.showerror("Error", "Task not found for deletion.", parent=self)
            self._refresh_task_list()
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task: '{task.title}'?", parent=self)
        if confirm:
            if self.task_manager.delete_task(selected_task_id):
                self._refresh_task_list()
                self._update_status_bar(f"Task '{task.title}' deleted.")
            else: # Deletion failed in backend for some reason
                messagebox.showerror("Error", "Failed to delete the task.", parent=self)
                self._refresh_task_list()

    def _toggle_selected_task_completion(self) -> None:
        """Toggles the completion status of the selected task."""
        selected_task_id = self._get_selected_task_id()
        if not selected_task_id:
            messagebox.showerror("Error", "No task selected. Please select a task to toggle completion.", parent=self)
            return

        task_before_toggle = self.task_manager.get_task(selected_task_id)
        if not task_before_toggle: # Should not happen
            messagebox.showerror("Error", "Task not found for toggling.", parent=self)
            self._refresh_task_list()
            return

        if self.task_manager.toggle_complete(selected_task_id):
            self._refresh_task_list()
            # Status bar message should reflect the new state
            current_task_state = self.task_manager.get_task(selected_task_id)
            if current_task_state:
                 new_status_str = "Completed" if current_task_state.completed else "Pending"
                 self._update_status_bar(f"Task '{current_task_state.title}' marked as {new_status_str}.")
            else: # Task somehow disappeared after toggle, refresh and generic message
                 self._update_status_bar(f"Task completion status toggled.")
        else:
            messagebox.showerror("Error", "Failed to toggle task completion.", parent=self)
            self._refresh_task_list()

    def _on_task_select(self, event: Optional[Any] = None) -> None: # event from TreeviewSelect
        """Callback for when a task selection changes in the Treeview."""
        self._update_button_states()

    def _open_stats_window(self) -> None:
        """Opens the statistics window if tasks are available."""
        if not self.task_manager.get_all_tasks():
            messagebox.showinfo("Statistics", "No tasks available to generate statistics.", parent=self)
            return
        StatsWindow(self, self.task_manager)

    def _update_button_states(self) -> None:
        """
        Enables or disables control buttons based on whether a task is selected
        and whether any tasks exist at all (for the stats button).
        """
        is_task_selected = self._get_selected_task_id() is not None
        any_tasks_exist = bool(self.task_manager.get_all_tasks())

        self.edit_button.config(state=tk.NORMAL if is_task_selected else tk.DISABLED)
        self.delete_button.config(state=tk.NORMAL if is_task_selected else tk.DISABLED)
        self.toggle_button.config(state=tk.NORMAL if is_task_selected else tk.DISABLED)
        self.stats_button.config(state=tk.NORMAL if any_tasks_exist else tk.DISABLED)

# Example of how to run (though this will be in main.py, kept for reference)
# if __name__ == "__main__":
#     # This setup is illustrative and would typically be in main.py
#     # Ensure tasks.json exists or is handled by TaskManager
#     try:
#         # Attempt to create tasks.json if it doesn't exist to avoid initial FileNotFoundError if desired
#         # However, TaskManager itself handles this by creating an empty list.
#         with open('tasks.json', 'a', encoding='utf-8') as f:
#             pass
#     except IOError:
#         print("Warning: Could not ensure tasks.json exists or is writable.")

#     task_mgr = TaskManager(filepath='tasks.json')
#     # Example: Add a dummy task if the list is empty for testing
#     # if not task_mgr.get_all_tasks():
#     #     task_mgr.add_task("Test Task", "This is a test", "Medium", datetime.now().strftime("%Y-%m-%d"))
#     app = MainApplication(task_mgr)
#     app.mainloop()
