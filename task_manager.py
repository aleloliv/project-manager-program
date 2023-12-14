# Welcome to the Task Manager Program!

# Overview:
# This program seamlessly integrates Project Management practices with Python coding and leverages a MySQL Database for efficient data storage. The Task Manager enables users to create, manage, and track projects and associated tasks, promoting organized collaboration and project development.

# Setup Instructions:
# To ensure smooth execution, please follow these steps:
# 1. Install MySQL Workbench.
# 2. Uncomment the SQL code provided below (select, Ctrl+K, Ctrl+C), execute it to create a SCHEMA, and then re-comment the code.
# 3. Note: Delete the SQL code from this file or comment it again before running the .py file.

# -- MySQL Workbench Forward Engineering

# SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
# SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
# SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

# -- -----------------------------------------------------
# -- Schema projects
# -- -----------------------------------------------------
# CREATE SCHEMA IF NOT EXISTS `projects` DEFAULT CHARACTER SET utf8 ;
# USE `projects` ;
# -- -----------------------------------------------------
# -- Table `projects`.`projects`
# -- -----------------------------------------------------
# DROP TABLE IF EXISTS `projects`.`projects` ;

# CREATE TABLE IF NOT EXISTS `projects`.`projects` (
#   `project_id` INT NOT NULL AUTO_INCREMENT,
#   `project_name` VARCHAR(100) NOT NULL,
#   `project_due_date` DATETIME NOT NULL,
#   `project_owner` VARCHAR(100) NOT NULL,
#   `project_type` VARCHAR(100) NOT NULL,
#   `allowed_files` VARCHAR(100) NOT NULL,
#   `project_scope` LONGTEXT NOT NULL,
#   PRIMARY KEY (`project_id`)
# ) ENGINE = InnoDB;

# -- -----------------------------------------------------
# -- Table `projects`.`tasks`
# -- -----------------------------------------------------
# DROP TABLE IF EXISTS `projects`.`tasks` ;

# CREATE TABLE IF NOT EXISTS `projects`.`tasks` (
#   `task_id` INT NOT NULL AUTO_INCREMENT,
#   `task_name` VARCHAR(100) NOT NULL,
#   `task_description` VARCHAR(255) NOT NULL,
#   `task_start` DATETIME NOT NULL,
#   `task_end` DATETIME NOT NULL,
#   `project_id` INT NOT NULL,
#   PRIMARY KEY (`task_id`),
#   INDEX `fk_tasks_projects_idx` (`project_id` ASC) VISIBLE,
#   CONSTRAINT `fk_tasks_projects`
#     FOREIGN KEY (`project_id`)
#     REFERENCES `projects`.`projects` (`project_id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION
# ) ENGINE = InnoDB;

# -- -----------------------------------------------------
# -- Table `projects`.`designers`
# -- -----------------------------------------------------
# DROP TABLE IF EXISTS `projects`.`designers` ;

# CREATE TABLE IF NOT EXISTS `projects`.`designers` (
#   `designer_id` INT NOT NULL AUTO_INCREMENT,
#   `designer_name` VARCHAR(100) NOT NULL,
#   PRIMARY KEY (`designer_id`)
# ) ENGINE = InnoDB;

# -- -----------------------------------------------------
# -- Table `projects`.`assigned_designer`
# -- -----------------------------------------------------
# DROP TABLE IF EXISTS `projects`.`assigned_designer` ;

# CREATE TABLE IF NOT EXISTS `projects`.`assigned_designer` (
#   `designer_id` INT NOT NULL,
#   `task_id` INT NOT NULL,
#   PRIMARY KEY (`designer_id`, `task_id`),
#   INDEX `fk_assigned_designer_tasks1_idx` (`task_id` ASC) VISIBLE,
#   INDEX `fk_assigned_designer_designers1_idx` (`designer_id` ASC) VISIBLE,
#   CONSTRAINT `fk_assigned_designer_designers1`
#     FOREIGN KEY (`designer_id`)
#     REFERENCES `projects`.`designers` (`designer_id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_assigned_designer_tasks1`
#     FOREIGN KEY (`task_id`)
#     REFERENCES `projects`.`tasks` (`task_id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION
# ) ENGINE = InnoDB;

# DROP TABLE IF EXISTS `projects`.`formats` ;

# CREATE TABLE IF NOT EXISTS `projects`.`formats` (
# 	`format_id` INT NOT NULL AUTO_INCREMENT,
#     `file_format` VARCHAR(10) NOT NULL,
#     `project_id` INT NOT NULL,
#     PRIMARY KEY(`format_id`),
# 	INDEX `fk_formats_projects_idx` (`project_id` ASC) VISIBLE,
# 	CONSTRAINT `fk_formats_projects`
# 		FOREIGN KEY (`project_id`)
#         REFERENCES `projects`.`projects` (`project_id`)
# 		ON DELETE NO ACTION
# 		ON UPDATE NO ACTION
# ) ENGINE = InnoDB;

# SET SQL_MODE=@OLD_SQL_MODE;
# SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
# SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


# Running the Program:
# Execute this Python file after configuring the database. The program's intuitive interface allows you to create new projects, add tasks, and view project details effortlessly.

# Dependencies:
# Ensure you have the necessary libraries installed, including datetime, tkinter, ttk, messagebox, simpledialog, and pymysql (this is the most important one to make use of the MySQL database, it shouldn't be too hard to install).

# To install the PyMySQL module, you can use the pip tool, which is the package installer for Python.

# Option 1: Using Command Line
# Open your command prompt or terminal and run the following command:
# pip install pymysql
# This command will download and install the PyMySQL module and its dependencies.

# Option 2: Using a Jupyter Notebook or Python Script
# If you are using a Jupyter notebook or a Python script, you can install PyMySQL within your notebook or script.
# Add the following line at the beginning:
# !pip install pymysql
# Then run the cell in the Jupyter notebook or execute the script.

# Option 3: Using a Virtual Environment
# If you are working within a virtual environment, activate your virtual environment and then use the pip command as shown in Option 1.

# Verification
# After installation, you can verify that PyMySQL is installed correctly by trying to import it in your Python script or interactive environment:
# import pymysql
# If no errors occur, the installation was successful.

# Remember to install PyMySQL in the Python environment where you plan to run your Task Manager program.
# If you're using a specific Python version or environment, ensure that pip corresponds to that Python version or environment.

# Now you should be all set to use PyMySQL in your Task Manager program!

# Let's get started! Run the program and enhance your project management experience.

# Import necessary libraries
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pymysql

# Global declarations
window = None
project_type_combobox = None
create_task_button = None

conn = pymysql.connect(user='root', password='06101994', host='localhost', database='projects', port=3306)

# Date and time format
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Function to create a database connection
def create_db_connection():
    try:
        conn = pymysql.connect(user='root', password='06101994', host='localhost', database='projects', port=3306)
        return conn
    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error creating database connection: {e}")
        return None

# Function to close the database connection
def close_db_connection(conn):
    if conn:
        conn.close()

# Function to commit changes to the database
def commit_changes(conn):
    if conn:
        conn.commit()
        print("Changes committed to the database.")

# Function to fetch project names from the database
def get_project_names(conn):
    try:
        query = "SELECT project_name FROM projects;"
        with conn.cursor() as cursor:
            cursor.execute(query)
            projects = cursor.fetchall()
        return [project[0] for project in projects]
    except Exception as e:
        print(f"Error fetching project names: {e}")
        return []

# Function to fetch tasks for a given project from the database
def get_tasks_for_project(conn, project_id):
    try:
        query = "SELECT * FROM tasks WHERE project_id = %s;"
        with conn.cursor() as cursor:
            cursor.execute(query, (project_id,))
            tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching tasks for project: {e}")
        return []

# Function to create a new project
def create_new_project(conn, main_window):
    # Default values
    name = "New Project"
    owner = "Default"
    project_type = "Default"

    # Create a new window for project creation
    project_window = tk.Toplevel(main_window)
    project_window.title("Create New Project")

    # Labels and Entry widgets for project details
    tk.Label(project_window, text="Project Owner (press Enter to use default):").pack()
    owner_entry = tk.Entry(project_window)
    owner_entry.insert(0, owner)
    owner_entry.pack()

    tk.Label(project_window, text="Project Type (press Enter to use default):").pack()
    project_type_entry = tk.Entry(project_window)
    project_type_entry.insert(0, project_type)
    project_type_entry.pack()

    tk.Label(project_window, text="Project Name (press Enter to use default):").pack()
    name_entry = tk.Entry(project_window)
    name_entry.pack()

    tk.Label(project_window, text="Due Date (YYYY-MM-DD HH:mm:ss, press Enter to use default):").pack()
    due_date_entry = tk.Entry(project_window)
    due_date_entry.pack()

    tk.Label(project_window, text="Enter the filename for the project scope (press Enter to use default):").pack()
    scope_filename_entry = tk.Entry(project_window)
    scope_filename_entry.insert(0, "default_scope.txt")
    scope_filename_entry.pack()

    tk.Label(project_window, text="Insert file format:").pack()
    allowed_file_entry = tk.Entry(project_window)
    allowed_file_entry.pack()

    # Function to handle project creation
    def create_project():
        nonlocal name, owner, project_type

        # Get user input from entry widgets
        owner = owner_entry.get() or owner
        project_type = project_type_entry.get() or project_type
        name = name_entry.get() or name
        due_date_input = due_date_entry.get()
        if not due_date_input:
            due_date = datetime.now()
        else:
            try:
                due_date = datetime.strptime(due_date_input, DATETIME_FORMAT)
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please enter a valid date.")
                return

        scope_filename = scope_filename_entry.get() or "default_scope.txt"
        scope = read_project_scope(scope_filename)

        allowed_file = allowed_file_entry.get()

        # Validate input
        if not name or not owner or not project_type:
            messagebox.showerror("Error", "Name, owner, and project type are required fields.")
            return

        # Perform validation and database insertion logic here
        insert_project_query = """
            INSERT INTO projects (project_name, project_due_date, project_owner, project_type, project_scope, allowed_files) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        project_data = (name, due_date, owner, project_type, scope, allowed_file)

        with conn.cursor() as cursor:
            try:
                cursor.execute(insert_project_query, project_data)
                project_id = cursor.lastrowid
                conn.commit()  # Commit changes immediately
            except pymysql.Error as e:
                messagebox.showerror("Error", f"Error creating project: {e}")
                return

        # Display a messagebox indicating successful project creation
        messagebox.showinfo("Success", "Project created successfully!")

        # Close the project window
        project_window.destroy()

    # Button to create the project
    create_button = tk.Button(project_window, text="Create Project", command=create_project)
    create_button.pack()

# Function to read the content of a project scope file
def read_project_scope(filename):
    try:
        with open(filename, 'r') as scope_file:
            read_project_scope_content = scope_file.read()
    except FileNotFoundError:
        messagebox.showwarning("Warning", f"File {filename} not found. Using an empty scope.")
        read_project_scope_content = ""
    return read_project_scope_content

# Function to create a new task window
def create_new_task_window(conn, project_combobox):
    new_task_window = tk.Toplevel(window)
    new_task_window.title("Create New Task")

    # Dropdown list with available projects
    tk.Label(new_task_window, text="Select Project:").pack()
    project_names = get_project_names(conn)
    project_combobox = ttk.Combobox(new_task_window, values=project_names)
    project_combobox.set("Select Project")
    project_combobox.pack()

    # Form to insert info for a new task
    tk.Label(new_task_window, text="Task Name:").pack()
    task_name_entry = tk.Entry(new_task_window)
    task_name_entry.pack()

    tk.Label(new_task_window, text="Task Description:").pack()
    task_description_entry = tk.Entry(new_task_window)
    task_description_entry.pack()

    tk.Label(new_task_window, text="Task Start Date (YYYY-MM-DD HH:mm:ss):").pack()
    task_start_entry = tk.Entry(new_task_window)
    task_start_entry.pack()

    tk.Label(new_task_window, text="Task End Date (YYYY-MM-DD HH:mm:ss):").pack()
    task_end_entry = tk.Entry(new_task_window)
    task_end_entry.pack()

    # Button to view all tasks for the selected project
    def view_tasks():
        selected_project = project_combobox.get()
        if selected_project == "Select Project":
            messagebox.showwarning("Warning", "Please select a project.")
            return

        project_id = get_project_id(conn, selected_project)
        tasks = get_tasks_for_project(conn, project_id)

        if not tasks:
            messagebox.showinfo("Info", "No tasks found for the selected project.")
        else:
            task_details = "\n".join([f"Task ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Start Date: {task[3]}, End Date: {task[4]}" for task in tasks])
            messagebox.showinfo("All Tasks", task_details)

    # Button to add task to project
    def add_task_to_project():
        selected_project = project_combobox.get()
        if selected_project == "Select Project":
            messagebox.showwarning("Warning", "Please select a project.")
            return

        project_id = get_project_id(conn, selected_project)

        name = task_name_entry.get()
        description = task_description_entry.get()
        task_start_input = task_start_entry.get()
        task_end_input = task_end_entry.get()

        # Convert date strings to datetime objects
        try:
            task_start = datetime.strptime(task_start_input, DATETIME_FORMAT)
            task_end = datetime.strptime(task_end_input, DATETIME_FORMAT)
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please enter a valid date.")
            return

        task_data = (name, description, task_start, task_end, project_id)

        insert_task_query = """
            INSERT INTO tasks (task_name, task_description, task_start, task_end, project_id) 
            VALUES (%s, %s, %s, %s, %s);
        """

        with conn.cursor() as cursor:
            try:
                cursor.execute(insert_task_query, task_data)
                conn.commit()
                messagebox.showinfo("Success", "Task added to the project successfully!")
                new_task_window.destroy()  # Close the window after successful task creation
            except pymysql.Error as e:
                messagebox.showerror("Error", f"Error adding task to project: {e}")

    tk.Button(new_task_window, text="View Tasks", command=view_tasks).pack()
    tk.Button(new_task_window, text="Add Task to Project", command=add_task_to_project).pack()

# Function to create a new task
def create_new_task(conn, project_combobox):
    # Open the task creation window
    create_new_task_window(conn, project_combobox)

# Function to view all tasks for a selected project
def view_all_tasks(conn, project_combobox):
    project_id = None
    if project_combobox.get() != "Select Project":
        project_name = project_combobox.get()
        project_id = get_project_id(conn, project_name)

    if project_id is None:
        messagebox.showwarning("Warning", "Please select a project first.")
        return

    query = "SELECT * FROM tasks WHERE project_id = %s;"
    with conn.cursor() as cursor:
        cursor.execute(query, (project_id,))
        tasks = cursor.fetchall()

    if not tasks:
        messagebox.showinfo("Info", "No tasks found for the selected project.")
    else:
        task_details = "\n".join([f"Task ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Start Date: {task[3]}, End Date: {task[4]}" for task in tasks])
        messagebox.showinfo("All Tasks", task_details)

# Function to fetch the project ID based on the project name
def get_project_id(conn, project_name):
    try:
        query = "SELECT project_id FROM projects WHERE project_name = %s;"
        with conn.cursor() as cursor:
            cursor.execute(query, (project_name,))
            result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching project ID: {e}")
        return None

# Function to commit changes to the database
def commit(conn):
    # Commit changes to the database
    conn.commit()
    print("Changes committed to the database.")

# Function to handle the event of selecting a project in the combobox
def on_combobox_select(event, project_combobox, project_details_label, create_task_button, conn):
    selected_project_name = project_combobox.get()
    if selected_project_name != "Select Project":
        selected_project = get_project_details(conn, selected_project_name)
        project_details_label.config(text=selected_project)
        create_task_button.config(state=tk.NORMAL)  # Enable the create task button
    else:
        # No project selected, update project details label accordingly
        project_details_label.config(text='No project selected.')
        create_task_button.config(state=tk.DISABLED)  # Disable the create task button

# Function to create the main window instance
def window_instance(conn):
    global window, project_type_combobox, create_task_button  # Add create_task_button to global

    if window is None:
        window = tk.Tk()
        window.title("Project Manager")

        def refresh_project_names():
            project_names = get_project_names(conn)
            project_type_combobox['values'] = project_names
            project_type_combobox.set("Select Project")

        # Frame using pack manager
        frame1 = tk.Frame(window)
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame using grid manager
        frame2 = tk.Frame(window)
        frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Button to create a new project
        button1 = tk.Button(frame2, text="Create New Project", command=lambda: [refresh_project_names(), create_new_project(conn, window)])
        button1.grid(row=0, column=0, padx=(0, 10), pady=(20, 0))

        # Entry field for typing the project name
        project_name_entry = tk.Entry(frame2)
        project_name_entry.grid(row=0, column=2, padx=(10, 0), pady=(20, 0))

        # Button to select a project
        button2 = tk.Button(frame2, text="Select Project", command=lambda: [refresh_project_names(), select_project(project_name_entry, conn, project_type_combobox, project_details_label, create_task_button)])
        button2.grid(row=0, column=3, pady=(20, 0))

        # Combobox for project names (fetching from the database)
        project_names = get_project_names(conn)
        project_type_combobox = ttk.Combobox(frame2, values=project_names)
        project_type_combobox.set("Select Project")  # Default text
        project_type_combobox.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        project_type_combobox.bind("<<ComboboxSelected>>", lambda event=None: on_combobox_select(event, project_type_combobox, project_details_label, create_task_button, conn))

        # Label to display project details
        project_details_label = tk.Label(frame2, text="", justify=tk.LEFT)
        project_details_label.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Button to create a new task
        create_task_button = tk.Button(frame2, text="Create New Task", command=lambda: [refresh_project_names(), create_new_task(conn, project_type_combobox)])
        create_task_button.grid(row=1, column=2, padx=(10, 0), pady=(20, 0))
        create_task_button.config(state=tk.NORMAL)  # Enable the create task button

        # Button to view all tasks for a selected project
        view_tasks_button = tk.Button(frame2, text="View All Tasks", command=lambda: view_all_tasks(conn, project_type_combobox))
        view_tasks_button.grid(row=1, column=3, pady=(20, 0))

        # Button to commit changes to the database
        commit_button = tk.Button(frame2, text="Commit Changes", command=lambda: commit_changes(conn))
        commit_button.grid(row=2, column=2, padx=(10, 0), pady=(10, 0))

        # Button to close the database connection and exit the application
        exit_button = tk.Button(frame2, text="Exit", command=lambda: [close_db_connection(conn), window.destroy()])
        exit_button.grid(row=2, column=3, pady=(10, 0))

        window.protocol("WM_DELETE_WINDOW", lambda: [close_db_connection(conn), window.destroy()])  # Ensure database connection is closed on window close

        window.mainloop()

        return window

# Function to fetch detailed information about a project
def get_project_details(conn, project_name):
    try:
        query = "SELECT * FROM projects WHERE project_name = %s;"
        with conn.cursor() as cursor:
            cursor.execute(query, (project_name,))
            result = cursor.fetchone()
        
        if result:
            project_id, name, due_date, owner, project_type, allowed_files, project_scope = result
            details = f"Project ID: {project_id}\nName: {name}\nDue Date: {due_date}\nOwner: {owner}\nProject Type: {project_type}\nAllowed Files: {allowed_files}\nScope: {project_scope}"
            return details
        else:
            return "Project details not found."

    except Exception as e:
        print(f"Error fetching project details: {e}")
        return "Error fetching project details."

# Function to select a project based on user input
def select_project(entry, conn, combobox, details_label, create_task_button):
    project_name = entry.get()
    if project_name:
        project_names = get_project_names(conn)
        if project_name in project_names:
            combobox.set(project_name)
            selected_project = get_project_details(conn, project_name)
            details_label.config(text=selected_project)
            create_task_button.config(state=tk.NORMAL)  # Enable the create task button
        else:
            messagebox.showwarning("Warning", "Project not found. Please enter a valid project name.")
    else:
        messagebox.showwarning("Warning", "Please enter a project name.")

# Main function to start the application
def main():
    # Create a database connection
    connection = create_db_connection()

    if connection:
        # Create the main window instance
        window = window_instance(connection)

if __name__ == "__main__":
    main()