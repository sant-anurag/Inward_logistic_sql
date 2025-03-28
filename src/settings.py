from common_utils import *


class SettingsWindow:
    # Constructor method initializes the Settings window with necessary UI components
    def __init__(self, parent):
        # Initialize variables that will store UI elements for project settings
        self.entry_modify_project = None  # Input field for modifying an existing project
        self.project_dropdown = None  # Dropdown to select existing projects
        self.project_list = None  # List of available projects
        self.entry_project_name = None  # Input field for entering a new project name

        # Store the reference to the parent window (main application window)
        self.parent = parent

        # Create a new top-level window as the settings window
        self.settings_window = Toplevel()

        # Get screen dimensions using pyautogui to position the window dynamically
        self.width, self.height = pyautogui.size()

        # Set the title of the settings window
        self.settings_window.title("Settings")

        # Define the size and position of the settings window
        # Width: 450, Height: 250, Positioned at 1/3 of the screen width, 1/3.2 of screen height
        self.settings_window.geometry(
            '{}x{}+{}+{}'.format(int('450'), int('250'), int(self.width / 3), int(self.height / 3.2))
        )

        # Set the background color of the settings window to 'wheat'
        self.settings_window.configure(bg='wheat')

        # Create a tab control (notebook) for organizing different settings sections
        self.tab_control = ttk.Notebook(self.settings_window)

        # Create the tab for project-related settings
        self.create_project_tab()

        # Create the tab for user-related settings
        self.create_user_tab()

        # Add the tab control to the settings window and allow it to expand
        self.tab_control.pack(expand=1, fill="both")

        # Start the event loop for the settings window to keep it open and responsive
        self.settings_window.mainloop()

    def create_project_tab(self):
        """
        This method creates the 'Project' tab in the application's UI.
        It includes UI elements for adding, modifying, and resetting projects.
        """

        # Create a new tab named "Project" with a background color of 'wheat'.
        tab_project = Frame(self.tab_control, bg='wheat')

        # Add the created frame as a tab in the tab control.
        self.tab_control.add(tab_project, text="Project")

        # -------- Master Frame for Layout Alignment --------
        # This master frame acts as a container for all project-related sections.
        frame_master = Frame(tab_project, bg='wheat')
        frame_master.grid(row=0, column=0, padx=5, pady=10, sticky="nw")

        # -------- Frame 1: Add Project Section --------
        # This frame is for adding a new project.
        frame_add_project = Frame(frame_master, bd=4, relief='ridge', bg='wheat')
        frame_add_project.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Label for 'Add Project' section.
        lbl_add_project = Label(frame_add_project, text="Add Project:", font=('ariel narrow', 12), bg='wheat')
        lbl_add_project.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Entry field for entering the new project name.
        self.entry_project_name = Entry(frame_add_project, width=43, font=('ariel narrow', 10), bg='light yellow')
        self.entry_project_name.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Frame for buttons related to project addition.
        frame_project_buttons = Frame(frame_add_project, bg='wheat')
        frame_project_buttons.grid(row=1, column=0, columnspan=2, pady=5)

        # Save button: Saves the entered project name.
        btn_save_project = Button(frame_project_buttons, text="Save", command=self.save_project,
                                  font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_save_project.grid(row=0, column=0, padx=5)

        # Modify button: Modifies the selected project.
        btn_modify_project = Button(frame_project_buttons, text="Modify", command=self.modify_project,
                                    font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_modify_project.grid(row=0, column=1, padx=5)

        # Reset button: Clears the project name entry field.
        btn_reset_project = Button(frame_project_buttons, text="Reset", command=self.reset_project,
                                   font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_reset_project.grid(row=0, column=2, padx=5)

        # -------- Frame 2: Modify Project Section --------
        # This frame is for modifying an existing project.
        frame_modify_project = Frame(frame_master, bd=4, relief='ridge', bg='wheat')
        frame_modify_project.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Label for 'Modify Project' section.
        lbl_modify_project = Label(frame_modify_project, text="Modify Project:", font=('ariel narrow', 12), bg='wheat')
        lbl_modify_project.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Dropdown list to select an existing project for modification.
        self.project_dropdown = ttk.Combobox(frame_modify_project, font=('ariel narrow', 10),
                                             state="readonly", width=38)  # Matches entry width.
        self.project_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Label for entering the new project name.
        lbl_new_project = Label(frame_modify_project, text="New Name:", font=('ariel narrow', 12), bg='wheat')
        lbl_new_project.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        # Entry field for modifying the selected project’s name.
        self.entry_modify_project = Entry(frame_modify_project, width=40, font=('ariel narrow', 10), bg='light yellow')
        self.entry_modify_project.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # -------- Modify Buttons --------
        # This frame contains buttons for modifying and exiting the project section.
        frame_modify_buttons = Frame(frame_modify_project, bg='wheat')
        frame_modify_buttons.grid(row=2, column=0, columnspan=2, pady=5)

        # Modify button: Updates the selected project name.
        btn_modify_project = Button(frame_modify_buttons, text="Modify", command=self.modify_project,
                                    font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_modify_project.grid(row=0, column=0, padx=5)

        # Exit button: Closes the settings window.
        btn_exit_project = Button(frame_modify_buttons, text="Exit", command=self.settings_window.destroy,
                                  font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_exit_project.grid(row=0, column=1, padx=5)

        # Ensures that the second column in frame_master stretches properly when resized.
        frame_master.grid_columnconfigure(1, weight=1)

        # Load existing projects into the dropdown list.
        self.load_projects()

    def save_project(self):
        """
        This method saves the entered project name to a file and updates the project list.
        It also provides feedback to the user based on whether the input is valid.
        """

        # Retrieves the text from the project name entry field and removes any leading/trailing whitespace.
        project_name = self.entry_project_name.get().strip()

        # Checks if the user has entered a non-empty project name.
        if project_name:
            # Opens the file 'projects.txt' in append mode ('a'), meaning new entries are added without overwriting existing data.
            with open("projects.txt", "a") as file:
                # Writes the project name to the file, followed by a newline to separate entries.
                file.write(project_name + "\n")

            # Displays a success message to inform the user that the project was added successfully.
            messagebox.showinfo("Success", "Project Added Successfully")

            # Clears the project name entry field after saving the project.
            self.entry_project_name.delete(0, END)

            # Calls a method to reload and update the project list, ensuring the new entry appears in the UI.
            self.load_projects()
        else:
            # Displays a warning message if the input field is empty or contains only spaces.
            messagebox.showwarning("Warning", "Enter a valid project name!")

    def modify_project(self):
        """
        This method modifies an existing project name in the 'projects.txt' file.
        It ensures that a project is selected and a new name is provided before updating the file.
        """

        # Retrieves the currently selected project name from the dropdown and removes leading/trailing whitespace.
        selected_project = self.project_dropdown.get().strip()

        # Retrieves the new project name entered by the user and removes leading/trailing whitespace.
        new_project_name = self.entry_modify_project.get().strip()

        # Prints the selected project and new project name to the console for debugging purposes.
        print("Selected Project : ", selected_project, "  New name : ", new_project_name)

        # If no project is selected, show a warning and exit the function early.
        if not selected_project:
            messagebox.showwarning("Warning", "No project selected!")
            return

        # If the new project name is empty, show a warning and exit the function early.
        if not new_project_name:
            messagebox.showwarning("Warning", "Enter a new project name!")
            return

        # Open 'projects.txt' in read mode and read all lines into a list.
        with open("projects.txt", "r") as file:
            projects = file.read().splitlines()  # Reads all lines and removes trailing newline characters.

        # Check if the selected project exists in the file.
        if selected_project in projects:
            # Create a new list where the selected project name is replaced with the new name.
            updated_projects = [new_project_name if project == selected_project else project for project in projects]

            # Open 'projects.txt' in write mode to overwrite it with updated project names.
            with open("projects.txt", "w") as file:
                file.write("\n".join(updated_projects) + "\n")  # Write the updated project list back to the file.

            # Show a success message to indicate that the project was modified.
            messagebox.showinfo("Success", "Project Modified Successfully")

            # Clear the project name entry field after modification.
            self.entry_project_name.delete(0, END)

            # Reload the project list to reflect the changes in the dropdown.
            self.load_projects()

            # If there are still projects in the list, set the first one as the default selection.
            if updated_projects:
                self.project_dropdown.set(updated_projects[0])
        else:
            # Show a warning message if the selected project is not found in the file.
            messagebox.showwarning("Warning", "Selected project not found!")

    def reset_project(self):
        """
        This method resets the project input fields in the GUI.
        It clears the project name entry field and resets the selected project list.
        """

        # Clears the text input field for project name.
        # The delete method removes text from the entry widget, from index 0 (start) to END (last character).
        self.entry_project_name.delete(0, END)

        # Resets the project list selection to an empty string.
        # This is likely a Tkinter StringVar associated with a dropdown (e.g., OptionMenu or Listbox).
        # Setting it to an empty string ensures that no project remains selected.
        self.project_list.set("")

    def load_projects(self):
        """
        Loads the list of projects from a text file and updates the project dropdown.

        This function checks if the "projects.txt" file exists:
        - If the file exists, it reads the list of project names and populates the dropdown menu.
        - If the file does not exist, it clears the dropdown selection.

        Steps:
        1. Check if "projects.txt" exists.
        2. If the file is found:
           - Read all project names from the file.
           - Assign these names to the project dropdown.
           - If at least one project is available, set the first project as the default selection.
        3. If the file does not exist:
           - Set an empty list for dropdown values.
           - Clear any existing selection.
        """

        # Check if the file "projects.txt" exists in the current directory
        if os.path.exists("projects.txt"):
            # Open the file in read mode and read all project names, removing newline characters
            with open("projects.txt", "r") as file:
                projects = file.read().splitlines()  # Read lines and remove newline characters

            # Update the dropdown list with the retrieved project names
            self.project_dropdown["values"] = projects

            # If there are any projects in the list, set the first one as the default selection
            if projects:
                self.project_dropdown.set(projects[0])
        else:
            # If the file does not exist, set an empty list for the dropdown menu
            self.project_dropdown["values"] = []
            # Clear any existing selection in the dropdown
            self.project_dropdown.set("")

    def create_user_tab(self):
        """
        Creates the 'User' tab in the application.

        This function is responsible for setting up the GUI elements required for user management.
        It includes input fields for username, password, and category selection, along with buttons
        for saving a user and exiting the tab.

        Steps:
        1. Create a new tab labeled 'User' and add it to the tab control.
        2. Create a frame for user management within the tab.
        3. Add labels and input fields for:
           - Username (Entry field)
           - Password (Entry field with masked input)
           - Category (Dropdown selection)
        4. Add a sub-frame for action buttons:
           - "Save User" to store user details.
           - "Exit" to close the settings window.

        """

        # Create a new tab named "User" and set its background color.
        tab_user = Frame(self.tab_control, bg='wheat')

        # Add the newly created tab to the tab control with the label "User".
        self.tab_control.add(tab_user, text="User")

        # Create a frame for user management inside the "User" tab.
        frame_user_management = Frame(tab_user, bd=4, relief='ridge', bg='wheat')
        frame_user_management.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        # Add a bold label for "User Management" at the top of the frame.
        lbl_user = Label(frame_user_management, text="User Management", font=('ariel narrow', 12, 'bold'), bg='wheat')
        lbl_user.grid(row=0, column=0, columnspan=2, pady=10)

        # Create a label and entry field for entering the username.
        lbl_username = Label(frame_user_management, text="Username:", font=('ariel narrow', 12), bg='wheat')
        lbl_username.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_username = Entry(frame_user_management, width=40, font=('ariel narrow', 10), bg='light yellow')
        self.entry_username.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Create a label and entry field for entering the password.
        lbl_password = Label(frame_user_management, text="Password:", font=('ariel narrow', 12), bg='wheat')
        lbl_password.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Password entry field with masked input (displayed as "*").
        self.entry_password = Entry(frame_user_management, width=40, font=('ariel narrow', 10), show="*",
                                    bg='light yellow')
        self.entry_password.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        # Create a label for category selection.
        lbl_category = Label(frame_user_management, text="Category:", font=('ariel narrow', 12), bg='wheat')
        lbl_category.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Define a StringVar to store the selected category.
        self.category_var = StringVar()
        self.category_var.set("User")  # Default selection is "User".

        # Create a dropdown (ComboBox) for selecting user categories (User/Admin).
        category_dropdown = ttk.Combobox(frame_user_management, textvariable=self.category_var, state="readonly",
                                         values=["User", "Admin"], font=('ariel narrow', 10), width=38)
        category_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="we")

        # Create a separate frame to hold user action buttons.
        frame_user_buttons = Frame(frame_user_management, bd=4, relief='ridge', bg='wheat')
        frame_user_buttons.grid(row=4, column=0, columnspan=2, pady=10)

        # "Save User" button to save the user details.
        btn_save_user = Button(frame_user_buttons, text="Save User", command=self.save_user, font=('ariel narrow', 10),
                               width=10, bg='light cyan')
        btn_save_user.grid(row=0, column=0, padx=5)

        # "Exit" button to close the settings window.
        btn_exit_user = Button(frame_user_buttons, text="Exit", command=self.settings_window.destroy,
                               font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_exit_user.grid(row=0, column=1, padx=5)

    def save_user(self):
        """
        Saves a new user to the 'Users.xlsx' file.

        This function retrieves the username, password, and category entered by the user in the GUI.
        If all fields are valid, it checks whether the 'Users.xlsx' file exists. If not, it creates a new file.
        The user details are then appended to the file, ensuring sequential numbering.

        Steps:
        1. Retrieve and sanitize input values.
        2. Validate that all fields are filled.
        3. Check if 'Users.xlsx' exists:
           - If not, create a new DataFrame with appropriate columns.
           - If yes, load existing data.
        4. Append new user details to the DataFrame.
        5. Save the updated DataFrame back to 'Users.xlsx'.
        6. Display success message and reset input fields.
        7. If validation fails, show a warning message.

        """

        # Retrieve the username, password, and category from input fields, removing any extra spaces.
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        category = self.category_var.get().strip()

        # Check if all input fields have valid values before proceeding.
        if username and password and category:
            file_path = "Users.xlsx"  # Define the file path for storing user data.

            # Check if the file exists. If not, create a new DataFrame with appropriate columns.
            if not os.path.exists(file_path):
                df = pd.DataFrame(columns=["S.No", "Username", "Password", "Category"])
            else:
                # Load the existing Excel file into a DataFrame.
                df = pd.read_excel(file_path)

            # Create a new entry DataFrame with incremented serial number.
            new_entry = pd.DataFrame([[len(df) + 1, username, password, category]],
                                     columns=["S.No", "Username", "Password", "Category"])

            # Append the new entry to the existing DataFrame.
            df = pd.concat([df, new_entry], ignore_index=True)

            # Save the updated DataFrame back to 'Users.xlsx' without index numbers.
            df.to_excel(file_path, index=False)

            # Display a success message indicating that the user has been created.
            messagebox.showinfo("Success", "User Created Successfully")

            # Reset input fields after successfully saving the user.
            self.entry_username.delete(0, END)  # Clear the username field.
            self.entry_password.delete(0, END)  # Clear the password field.
            self.category_var.set("User")  # Reset the category to the default value.

        else:
            # Show a warning if any field is missing or invalid.
            messagebox.showwarning("Warning", "Enter valid Username, Password, and select a Category!")

