# TkTask - Simple Task Management Application

TkTask is a desktop application built with Python and Tkinter that helps you manage your daily tasks efficiently. It provides a user-friendly interface to add, edit, delete, and track tasks, with features like prioritization, due dates, and completion status. Task data is stored locally in a JSON file. The application also offers basic data visualization for task statistics.

## Screenshots

*(Note: Actual screenshots would be inserted here in a real project.)*

1.  **Main Application Window:** Shows the primary interface with the task list (displaying title, priority, due date, status), control buttons (Add, Edit, Delete, Toggle Complete, View Statistics), and filter options (by priority and status).
2.  **Add/Edit Task Dialog:** A modal window with fields for entering or modifying task details: Title, Description, Priority (combobox), and Due Date. The "Completed" checkbox is visible in edit mode.
3.  **Task Statistics Window:** A modal window displaying task analytics:
    *   Summary counts (Total, Completed, Pending tasks).
    *   A bar chart showing the distribution of tasks by priority (Low, Medium, High).
    *   A pie chart illustrating the proportion of completed versus pending tasks.

## Features

*   **User-Friendly GUI:** Simple and intuitive interface built with Tkinter.
*   **Task Management:** Add new tasks, edit existing task details, and delete tasks.
*   **Task Prioritization:** Assign "High", "Medium", or "Low" priority to tasks.
*   **Due Dates:** Assign due dates to tasks (format: YYYY-MM-DD).
*   **Completion Tracking:** Mark tasks as "Completed" or "Pending".
*   **Data Persistence:** Tasks are saved locally in a `tasks.json` file, so your data persists between sessions.
*   **Filtering:** Filter the task list by priority level or completion status ("All", "Pending", "Completed").
*   **Data Visualization:** View statistics about your tasks, including:
    *   Counts of total, completed, and pending tasks.
    *   A bar chart showing the distribution of tasks by priority.
    *   A pie chart showing the ratio of completed to pending tasks.
    *   (Powered by Matplotlib)
*   **Error Handling:** User-friendly error messages for invalid inputs or issues.
*   **Cross-Platform:** Being a Python and Tkinter application, it should run on Windows, macOS, and Linux (provided Python and Tkinter are installed).

## Installation Instructions

### Prerequisites

*   **Python 3.7+:** Ensure you have Python 3.7 or a newer version installed. Tkinter is usually included with standard Python installations. You can download Python from [python.org](https://www.python.org/).
*   **`matplotlib`:** This package is required for displaying task statistics charts.

### Setting up a Virtual Environment (Recommended)

It's good practice to use a virtual environment to manage project dependencies.

1.  Open your terminal or command prompt.
2.  Navigate to the project directory where you've cloned or downloaded TkTask.
3.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4.  Activate the virtual environment:
    *   **On Windows:**
        ```bash
        venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    Your terminal prompt should change to indicate that the virtual environment is active (e.g., `(venv) ...`).

### Installing Dependencies

With your virtual environment activated, install the required package:

```bash
pip install matplotlib
```

## Usage Instructions

1.  Ensure you have completed the installation steps (Python, virtual environment, and dependencies).
2.  Navigate to the project's root directory in your terminal (if you're not already there).
3.  Make sure your virtual environment is activated.
4.  Run the application:
    ```bash
    python main.py
    ```
    The main application window should appear.

### Using the GUI:

*   **Adding a Task:** Click the "Add Task" button. Fill in the details in the dialog that appears and click "Save".
*   **Viewing Tasks:** Tasks are displayed in the main list. You can see their title, priority, due date, and status.
*   **Selecting a Task:** Click on a task in the list to select it.
*   **Editing a Task:** Select a task and click "Edit Selected", or double-click a task. Modify the details in the dialog and click "Save".
*   **Deleting a Task:** Select a task and click "Delete Selected". Confirm the deletion when prompted.
*   **Toggling Completion:** Select a task and click "Toggle Complete" to switch its status between "Pending" and "Completed".
*   **Filtering Tasks:**
    *   Use the "Priority" combobox to show tasks of a specific priority or "All" tasks.
    *   Use the "Status" combobox to show "Pending", "Completed", or "All" tasks.
*   **Viewing Statistics:** Click the "View Statistics" button to open a window with charts showing task distribution by priority and completion status, along with summary counts.

## Code Structure

The project is organized into the following key files:

*   `main.py`: The main entry point for the application. It initializes the `TaskManager` and the `MainApplication` GUI, and starts the Tkinter event loop.
*   `task_manager.py`: Contains the backend logic.
    *   `Task` class: Represents a single task with attributes like ID, title, description, priority, due date, and completion status.
    *   `TaskManager` class: Manages the collection of tasks, including adding, editing, deleting, loading from, and saving to the `tasks.json` file.
*   `gui.py`: Defines the Tkinter-based graphical user interface.
    *   `MainApplication` class: The main window of the application, displaying the task list, control buttons, and filters.
    *   `TaskDialog` class: A Toplevel window for adding new tasks or editing existing ones.
    *   `StatsWindow` class: A Toplevel window for displaying task statistics using Matplotlib charts.
*   `tasks.json`: The default JSON file where task data is stored. This file is automatically created in the same directory as `main.py` if it doesn't exist.

## Future Improvements

This application provides a solid foundation for task management. Potential future enhancements include:

*   **Due Date Reminders/Notifications:** Alert users about upcoming or overdue tasks.
*   **Enhanced Date Picker:** Use a more user-friendly calendar widget for selecting due dates instead of manual entry.
*   **Advanced Search & Sorting:** Allow searching tasks by keywords and more complex sorting options (e.g., sort by title).
*   **Customizable Themes:** Allow users to change the look and feel of the application.
*   **Export/Import Tasks:** Support exporting tasks to formats like CSV or iCalendar, and importing from them.
*   **Undo/Redo Functionality:** Allow users to revert actions like task deletion or modification.
*   **Sub-tasks:** Ability to create sub-tasks under a parent task.
*   **Recurring Tasks:** Option to define tasks that repeat on a schedule.
*   **User Accounts/Cloud Sync (Major):** For multi-user support or syncing across devices.

## License

This project is licensed under the MIT License.

MIT License

Copyright (c) 2024 The TkTask Project Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
