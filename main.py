"""
TkTask - Main Application Entry Point

This script initializes the TaskManager and the Tkinter-based GUI (MainApplication)
to run the task management application. It includes top-level error handling
for application startup and runtime issues.
"""
import tkinter as tk
from tkinter import messagebox
import sys
from gui import MainApplication
from task_manager import TaskManager


# Define the path for the tasks JSON file.
# Using a constant makes it clear and easy to change if needed.
TASKS_FILE_PATH = 'tasks.json'


def main() -> None:
    """
    Initializes and runs the TkTask application.

    This function sets up the TaskManager for backend data handling and
    then launches the MainApplication GUI. It incorporates error handling
    for critical failures during initialization or runtime.
    """
    tm_instance = None

    try:
        # Initialize TaskManager.
        # TaskManager's internal _load_tasks method handles FileNotFoundError
        # and json.JSONDecodeError by starting with an empty task list,
        # creating tasks.json if it doesn't exist upon first save.
        # This try-except block is for other unexpected critical errors during
        # TaskManager instantiation (e.g., permission issues, programming errors).
        tm_instance = TaskManager(filepath=TASKS_FILE_PATH)
    except Exception as e:
        error_title = "TaskManager Initialization Error"
        error_message = (
            f"A critical error occurred while initializing the Task Manager: {e}\n"
            "The application cannot continue and will now exit."
        )
        print(f"{error_title}: {error_message}", file=sys.stderr)

        try:
            # Attempt to show a Tkinter messagebox. A hidden root window is needed.
            root_err = tk.Tk()
            root_err.withdraw()  # Hide the blank root window
            messagebox.showerror(error_title, error_message)
            root_err.destroy()
        except tk.TclError:
            # Fallback if Tkinter itself has issues (e.g., no display server)
            print("Tkinter TclError: Could not display the error message GUI.", file=sys.stderr)
        except Exception as me:
            print(f"Error displaying messagebox: {me}", file=sys.stderr)
        sys.exit(1)  # Exit if TaskManager initialization fails

    # If tm_instance was successfully created, proceed to launch the GUI.
    # This check is technically redundant if sys.exit(1) is called above on error,
    # but provides an explicit safeguard.
    if tm_instance is None:
        # This block should ideally not be reached if the above sys.exit works.
        critical_error_msg = "TaskManager instance is None. Application cannot start."
        print(critical_error_msg, file=sys.stderr)
        root_fallback = tk.Tk()
        root_fallback.withdraw()
        messagebox.showerror("Critical Startup Error", critical_error_msg)
        root_fallback.destroy()
        sys.exit(1)

    try:
        app = MainApplication(task_manager_instance=tm_instance)
        app.mainloop()
    except Exception as e:
        # General catch-all for unexpected errors during GUI execution.
        error_title = "Application Runtime Error"
        error_message = f"An unexpected error occurred during application execution: {e}"
        print(f"{error_title}: {error_message}", file=sys.stderr)

        try:
            # Attempt to show error to user via messagebox.
            parent_window = None
            if 'app' in locals() and isinstance(app, tk.Tk) and app.winfo_exists():
                parent_window = app # Attach to app window if it still exists

            if parent_window:
                messagebox.showerror(error_title, error_message, parent=parent_window)
            else: # Fallback if app window not available
                root_err = tk.Tk()
                root_err.withdraw()
                messagebox.showerror(error_title, error_message)
                root_err.destroy()
        except tk.TclError:
            print("Tkinter TclError: Could not display the runtime error message GUI.", file=sys.stderr)
        except Exception as me:
            print(f"Error displaying runtime error messagebox: {me}", file=sys.stderr)
        sys.exit(1) # Exit on critical runtime error


if __name__ == "__main__":
    main()
