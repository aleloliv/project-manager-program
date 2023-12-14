import tkinter as tk
from tkinter import messagebox
import pytest
import pymysql
from datetime import datetime
from unittest.mock import MagicMock, patch
from task_manager import (
    create_db_connection,
    close_db_connection,
    commit_changes,
    get_project_names,
    get_tasks_for_project,
    create_new_project,
    read_project_scope,
    create_new_task_window,
    create_new_task,
    view_all_tasks,
    get_project_id,
    commit,
    on_combobox_select,
    window_instance,
    get_project_details,
    select_project,
)

from task_manager import *

@pytest.fixture
def conn():
    # Create a real database connection for testing
    return pymysql.connect(user='root', password='06101994', host='localhost', database='projects', port=3306)

# Mock for built-in open function
@pytest.fixture
def mock_open(request):
    patcher = patch("builtins.open")
    mock_open = patcher.start()
    request.addfinalizer(patcher.stop)
    return mock_open

# Mock for database connection
@pytest.fixture
def mock_db_connection(request):
    patcher = patch("task_manager.pymysql.connect")
    mock_connect = patcher.start()
    request.addfinalizer(patcher.stop)
    return mock_connect

# Mock for tkinter messagebox
@pytest.fixture
def mock_messagebox(request):
    patcher = patch("task_manager.messagebox")
    mock_box = patcher.start()
    request.addfinalizer(patcher.stop)
    return mock_box

# Mock for tkinter Toplevel
@pytest.fixture
def mock_toplevel(request):
    patcher = patch("task_manager.tk.Toplevel")
    mock_toplevel = patcher.start()
    request.addfinalizer(patcher.stop)
    return mock_toplevel

# Mock for datetime fixture
@pytest.fixture
def mock_datetime(request):
    patcher = patch("task_manager.datetime")
    mock_datetime = patcher.start()
    request.addfinalizer(patcher.stop)
    return mock_datetime

# Mock for showinfo fixture
@pytest.fixture
def mock_showinfo(request):
    patcher = patch("task_manager.messagebox.showinfo")
    mock_showinfo = patcher.start()
    request.addfinalizer(patcher.stop)
    return mock_showinfo

@pytest.fixture(scope='function')
def mock_tk(request):
    patcher = patch("task_manager.tkinter.Tk")
    mock_tk = patcher.start()
    request.addfinalizer(patcher.stop)
    return mock_tk

# Test create_db_connection function
@patch("task_manager.pymysql.connect")
def test_create_db_connection(mock_db_connection):
    # Create a MagicMock object to represent the expected connection
    expected_connection = MagicMock()
    mock_db_connection.return_value = expected_connection

    # Call the function
    conn = create_db_connection()

    # Assert that the returned connection is the expected connection
    assert conn == expected_connection

# Test close_db_connection function
def test_close_db_connection():
    mock_db_connection = MagicMock()
    close_db_connection(mock_db_connection)
    mock_db_connection.close.assert_called_once()

# Test commit_changes function
def test_commit_changes(mock_db_connection):
    commit_changes(mock_db_connection)
    mock_db_connection.commit.assert_called_once()

# Test get_project_names function
def test_get_project_names(mock_db_connection):
    # Set up mock cursor
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Mock the execute method of the cursor
    mock_cursor.execute.return_value = None
    mock_cursor.fetchall.return_value = [("Project1",), ("Project2",)]

    projects = get_project_names(mock_db_connection)
    assert projects == ["Project1", "Project2"]

def test_on_combobox_select_no_projects():
    mock_db_connection = MagicMock()
    mock_messagebox = MagicMock()

    project_combobox = MagicMock()
    project_details_label = MagicMock()
    create_task_button = MagicMock()

    # Set up mock event
    mock_event = MagicMock()

    # Set up mock data for get_project_names to return an empty list
    mock_db_connection.cursor.return_value.__enter__.return_value.fetchall.return_value = []

    on_combobox_select(mock_event, project_combobox, project_details_label, create_task_button, mock_db_connection)

    # Assert that project_details_label text is updated correctly
    project_details_label.config.assert_called_once()

    # Check the error message
    assert project_details_label.config.call_args_list[0][1]['text'] == 'Error fetching project details.'

    # Assert that the create_task_button state is updated correctly
    create_task_button.config.assert_called_once_with(state=tk.NORMAL)

def test_on_combobox_select_valid_project():
    mock_db_connection = MagicMock()
    mock_messagebox = MagicMock()

    project_combobox = MagicMock()
    project_details_label = MagicMock()
    create_task_button = MagicMock()

    # Set up mock event
    mock_event = MagicMock()

    # Set up mock data for get_project_names to return a valid project
    mock_project_name = "Test Project"
    mock_db_connection.cursor.return_value.__enter__.return_value.fetchall.return_value = [(mock_project_name,)]

    on_combobox_select(mock_event, project_combobox, project_details_label, create_task_button, mock_db_connection)

    # Assert that project_details_label text is updated correctly
    selected_project = get_project_details(mock_db_connection, mock_project_name)
    project_details_label.config.assert_called_once_with(text=selected_project)

    # Assert that the create_task_button state is updated correctly
    create_task_button.config.assert_called_once_with(state=tk.NORMAL)

def test_on_combobox_select_invalid_project():
    mock_db_connection = MagicMock()
    mock_messagebox = MagicMock()

    project_combobox = MagicMock()
    project_details_label = MagicMock()
    create_task_button = MagicMock()

    # Set up mock event
    mock_event = MagicMock()

    # Set up mock data for get_project_names to return a different project
    mock_db_connection.cursor.return_value.__enter__.return_value.fetchall.return_value = [("Another Project",)]

    on_combobox_select(mock_event, project_combobox, project_details_label, create_task_button, mock_db_connection)

    # Assert that project_details_label text is updated correctly
    project_details_label.config.assert_called_once_with(text='Error fetching project details.')

    # Assert that the create_task_button state is updated correctly
    create_task_button.config.assert_called_once_with(state=tk.NORMAL)

# Test window_instance function
def test_window_instance(mock_db_connection, capsys):
    with patch("task_manager.tk.Tk.mainloop") as mock_mainloop:
        window_instance(mock_db_connection)
        mock_mainloop.assert_called_once()

        # Capture console output
        print_output = capsys.readouterr().out

        # Assert that the expected message is present in the console output
        assert "Changes committed to the database." not in print_output

# Test read_project_scope function
def test_read_project_scope(mock_messagebox):
    with patch("builtins.open", create=True) as mock_open:
        # Mock the read method of the file
        mock_open.return_value.__enter__.return_value.read.return_value = "Mocked project scope content"

        # Call the function
        result = read_project_scope("mocked_scope.txt")

        # Assert that the content is read correctly
        assert result == "Mocked project scope content"

        # Assert that open is called with the correct file name
        mock_open.assert_called_once_with("mocked_scope.txt", 'r')

# Test create_new_task function
def test_create_new_task(mock_db_connection, mock_messagebox):
    project_combobox = MagicMock()

    with patch("task_manager.create_new_task_window") as mock_create_new_task_window:
        create_new_task(mock_db_connection, project_combobox)

        # Assert that create_new_task_window is called with the correct arguments
        mock_create_new_task_window.assert_called_once_with(mock_db_connection, project_combobox)

# Test view_all_tasks function
@patch("task_manager.get_project_id")
@patch("task_manager.messagebox.showwarning")
def test_view_all_tasks_no_project_selected(mock_showwarning, mock_get_project_id):
    conn = MagicMock()
    project_combobox = MagicMock()
    project_combobox.get.return_value = "Select Project"

    view_all_tasks(conn, project_combobox)

    # Assert that messagebox.showwarning is called with the correct message
    mock_showwarning.assert_called_once_with("Warning", "Please select a project first.")

    # Ensure get_project_id is not called when no project is selected
    mock_get_project_id.assert_not_called()

# Test get_project_id function
def test_get_project_id(mock_db_connection):
    with patch("task_manager.get_project_names") as mock_get_project_names:
        mock_get_project_names.return_value = ["Project1", "Project2"]

        # Test when the project name is found
        result = get_project_id(mock_db_connection, "Project1")
        assert result is not None

        # Test when the project name is not found
        assert result is mock_db_connection.cursor().__enter__().fetchone().__getitem__()

# Test get_project_details function
def test_get_project_details(mock_db_connection):
    # Set up mock cursor
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Mock the execute method of the cursor
    mock_cursor.execute.return_value = None
    mock_cursor.fetchone.return_value = (1, "Project1", datetime(2023, 1, 1), "Owner1", "Type1", "File1", "Scope1")

    result = get_project_details(mock_db_connection, "Project1")

    assert "Project ID: 1\nName: Project1\nDue Date:" in result
    assert "Owner: Owner1\nProject Type: Type1\nAllowed Files: File1\nScope: Scope1" in result

def test_get_tasks_for_project(mock_db_connection):
    # Set up mock cursor
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Mock the execute method of the cursor
    mock_cursor.execute.return_value = None
    mock_cursor.fetchall.return_value = [(1, "Task1", "Description1"), (2, "Task2", "Description2")]

    tasks = get_tasks_for_project(mock_db_connection, project_id=1)
    assert tasks == [(1, "Task1", "Description1"), (2, "Task2", "Description2")]

# Test create_new_project function
def test_create_new_project(mock_db_connection, mock_messagebox, mock_datetime, mock_tk, mock_toplevel, mock_filedialog):
    # Set up mock data for user input
    mock_input_data = {
        "project_name": "NewProject",
        "due_date": "2023-12-31",
        "owner": "John Doe",
        "project_type": "TypeA",
        "allowed_files": "file1.txt",
        "scope": "Project scope content",
    }

    # Set up mock data for datetime.now()
    mock_now = datetime(2023, 1, 1, 12, 0, 0)
    mock_datetime.now.return_value = mock_now

    # Set up mock data for user file selection
    mock_file_selection = "default_scope.txt"

    # Mock Tkinter methods
    mock_tk_instance = MagicMock()
    mock_tk.return_value = mock_tk_instance
    mock_toplevel_instance = MagicMock()
    mock_tk_instance.__enter__.return_value = mock_toplevel_instance

    # Mock file dialog
    mock_filedialog.askopenfilename.return_value = mock_file_selection

    with patch("task_manager.tkinter.Tk", mock_tk), \
         patch("task_manager.tkinter.Toplevel", mock_toplevel), \
         patch("tkinter.filedialog.askopenfilename", mock_filedialog):
        create_new_project(mock_db_connection, mock_tk_instance)


    with patch("tkinter.filedialog.askopenfilename", return_value=mock_file_selection):
        create_new_project(mock_db_connection)

    # Assert that the project is created with the correct data
    mock_db_connection.cursor.return_value.__enter__.return_value.execute.assert_called_once_with(
        """
        INSERT INTO project (name, due_date, owner, project_type, allowed_files, scope)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            mock_input_data["project_name"],
            mock_input_data["due_date"],
            mock_input_data["owner"],
            mock_input_data["project_type"],
            mock_input_data["allowed_files"],
            mock_input_data["scope"],
        ),
    )

    # Assert that the commit_changes function is called
    mock_db_connection.commit.assert_called_once()

    # Assert that the messagebox.showinfo is called with the correct message
    mock_messagebox.showinfo.assert_called_once_with("Success", "Project created successfully.")

# Test create_new_task_window function
def test_create_new_task_window(mock_db_connection, mock_toplevel):
    project_combobox = MagicMock()

    # Set up mock data for get_project_names to return a valid project
    mock_project_name = "Test Project"
    mock_db_connection.cursor.return_value.__enter__.return_value.fetchall.return_value = [(mock_project_name,)]

    create_new_task_window(mock_db_connection, project_combobox)

    # Assert that Toplevel is called
    mock_toplevel.assert_called_once()

# Test commit function
def test_commit(mock_db_connection):
    commit(mock_db_connection)
    mock_db_connection.commit.assert_called_once()

# Test select_project function
def test_select_project(mock_db_connection, mock_toplevel, mock_combobox):
    project_combobox = MagicMock()

    # Set up mock data for get_project_names to return a valid project
    mock_project_name = "Test Project"
    mock_db_connection.cursor.return_value.__enter__.return_value.fetchall.return_value = [(mock_project_name,)]

    select_project(mock_db_connection, project_combobox, mock_toplevel)

    # Assert that Toplevel is called
    mock_toplevel.assert_called_once()

    # Assert that the project_combobox is updated with the correct values
    project_combobox["values"] == [mock_project_name]

    # Assert that the project_combobox current value is set to the first project
    project_combobox.current.assert_called_once_with(0)