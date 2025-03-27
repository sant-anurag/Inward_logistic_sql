from search import *
from settings import *
from entry import *

class Logistics:
    """
    A class to manage logistics operations, such as tracking shipments, managing inventory,
    and handling inward entries. This class is designed to work with a GUI framework Tkinter
    and allows for the creation of the main window for logistics management.

    Attributes:
    master (tk.Tk): The main window of the GUI, which is used to display the application interface.
    """

    def __init__(self, master):
        """
        Constructor to initialize the Logistics object and create the main window for the logistics system.

        Parameters:
        master (tk.Tk): The root window or master widget passed to the Logistics object, which will be
                         used to create the main window for the GUI.

        This method initializes the instance and sets up the main window for the application.
        The main window is where various GUI components such as labels, buttons, and data displays
        will be placed.
        """
        self.main_window(master)

    def initialize_database(self):
        """
        Function to initialize the database (Excel file) for storing inward logistics data.

        This function ensures that a specific folder structure and an Excel workbook exist.
        If the Excel file does not exist, it creates a new one with predefined sheets and formatting.

        The Excel file stores inward material details, including supplier information,
        material description, project details, and signatures.

        Steps:
        1. Define the folder path where the file will be stored (OneDrive location).
        2. Create the folder if it does not already exist.
        3. Check if the Excel file exists.
        4. If the file exists, print a message and exit.
        5. If the file does not exist, create a new Excel workbook.
        6. Add a sheet with appropriate column headers.
        7. Apply formatting to the headers (font, color, border, alignment).
        8. Save the workbook.

        Returns:
        None
        """

        # Construct the full path to the OneDrive directory where the database will be stored.
        # This ensures that the file is saved in a centralized location.
        onedrive_path = os.path.join(os.environ["USERPROFILE"], "OneDrive - FORVIA")
        folder_path = os.path.join(onedrive_path, "Inward_logistic_master")
        file_name = os.path.join(folder_path, "Inward Material Register.xlsx")

        # Print the file path for debugging purposes.
        print(file_name)

        # Create the target directory if it does not exist.
        # The `exist_ok=True` parameter prevents errors if the directory already exists.
        os.makedirs(folder_path, exist_ok=True)

        # Check if the Excel file already exists to avoid overwriting existing data.
        if os.path.isfile(file_name):
            print("File already exists")  # Log message indicating no new file creation.
        else:
            # Create a new Excel workbook (spreadsheet).
            workbook = Workbook()

            # The first sheet in the workbook is active by default.
            # Rename this sheet to "Inward Entry" for clarity.
            sheet1 = workbook.active
            sheet1.title = "Inward Entry"

            # Define the column headers for the "Inward Entry" sheet.
            columns = database_columns

            # Define formatting for the header row:
            # - `header_font`: Sets font style, size, and boldness.
            # - `header_fill`: Sets a background fill color (light blue).
            header_font = Font(name='Bookman Old Style', size=11, bold=True)
            header_fill = PatternFill(start_color="87CEEB", end_color="87CEEB", fill_type="solid")

            # Define border styles:
            # - `thin_border`: Applies a thin border to normal cells.
            # - `thick_border`: Applies a thicker border for the header row.
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            thick_border = Border(
                left=Side(style='thick'),
                right=Side(style='thick'),
                top=Side(style='thick'),
                bottom=Side(style='thick')
            )

            # Function to set up a sheet by applying headers, formatting, and alignment.
            def setup_sheet(sheet):
                """
                Applies styling, formatting, and column width settings to a given worksheet.

                Parameters:
                sheet (Worksheet): The worksheet to apply formatting to.

                Returns:
                None
                """

                # Append column headers to the first row of the sheet.
                sheet.append(columns)

                # Define column widths corresponding to each column header.
                column_widths = [12, 12,12, 10, 8, 15, 12, 10, 10,8,8, 20, 25, 8, 12, 15, 12, 15, 15, 15, 20]

                # Apply formatting to header row (first row).
                for i, cell in enumerate(sheet[1], start=1):
                    cell.font = header_font  # Set bold font style.
                    cell.fill = header_fill  # Apply background color.
                    cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')  # Center align text.
                    sheet.column_dimensions[cell.column_letter].width = column_widths[i - 1]  # Adjust column width.
                    cell.border = thin_border  # Apply thin border.

                # Apply thin border to all cells in the sheet.
                for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, min_col=1, max_col=len(columns)):
                    for cell in row:
                        cell.border = thin_border  # Apply thin border to all cells.

                # Apply thick border to the header row for better visibility.
                for cell in sheet[1]:
                    cell.border = thick_border  # Apply thick border to header row.

            # Apply formatting setup to the "Inward Entry" sheet.
            setup_sheet(sheet1)

            # Save the workbook to the specified file path.
            workbook.save(filename=file_name)
            print("File created successfully")  # Log message indicating successful file creation.

    def data_entry_window(self,master):
        obj_dataEntry = DataEntryWindow(master)

    def search_window(self,master):
        obj_search = SearchWindow(master,None)

    def settings_window(self,master):
        obj_settings = SettingsWindow(master)

    def validate_numeric_input(self,input_str):
        """
        Function to validate whether the given input string is numeric.

        This function checks if the provided input string is a valid numeric value
        using the helper function `is_valid_numeric_input()`. It also allows an empty
        string as valid input (useful for clearing the field).

        If the input is not numeric, it displays an error message in a Tkinter message box.

        Parameters:
        input_str (str): The user-provided input string that needs validation.

        Returns:
        bool:
            - True if the input is a valid numeric value or an empty string.
            - False if the input is invalid (non-numeric), with an error message displayed.
        """

        # Check if the input string is a valid numeric value using the helper function
        # or if it's an empty string (empty string is allowed for field clearing)
        if is_valid_numeric_input(input_str) or input_str == "":
            return True  # Return True, allowing the input

        else:
            return False  # Return False, rejecting the input

    def download_inward_register(self,filetype):
        onedrive_path = os.path.join(os.environ["USERPROFILE"], "OneDrive - FORVIA")
        source_folder_path = os.path.join(onedrive_path, "Inward_logistic_master")
        if filetype == "master":
            file_name = "Inward Material Register.xlsx"
        elif filetype =="filterdata":
            donothing(None)
        source_path = os.path.join(source_folder_path, file_name)

        print("download_inward_register-> ", source_path)

        # Get user's default download directory
        download_dir = str(Path.home() / "Downloads")
        destination_path = os.path.join(download_dir, file_name)

        if os.path.exists(source_path):
            try:
                shutil.copy(source_path, destination_path)
                messagebox.showinfo("Success", f"'{file_name}' has been downloaded successfully to {download_dir}")
                # Open the Downloads directory in File Explorer
                # Open the Downloads directory in File Explorer, handle errors
                try:
                    subprocess.Popen(["explorer", download_dir], shell=True)
                except Exception as e:
                    print(f"Warning: Failed to open Downloads directory: {e}")

                # Open the downloaded Excel file
                try:
                    os.startfile(destination_path)  # Works on Windows
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open the file: {str(e)}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to download the file: {str(e)}")
        else:
            messagebox.showerror("Error", f"'{source_path}' does not exist.")

    def download_filteredData(self,file_name, status_label):
        source_path = file_name

        print("download_filteredData-> ", source_path)

        # Get user's default download directory
        download_dir = str(Path.home() / "Downloads")
        destination_path = os.path.join(download_dir, "Filtered_Inward_Material.xlsx")

        if os.path.exists(source_path):
            try:
                shutil.copy(source_path, destination_path)
                status_label.config(text="Download Success !!!", fg="green")
                # messagebox.showinfo("Success", f"'{file_name}' has been downloaded successfully to {download_dir}")
                # Open the Downloads directory in File Explorer
                # Open the Downloads directory in File Explorer, handle errors
                '''
                try:
                    subprocess.Popen(["explorer", download_dir], shell=True)
                except Exception as e:
                    print(f"Warning: Failed to open Downloads directory: {e}")

                # Open the downloaded Excel file
                try:
                    os.startfile(destination_path)  # Works on Windows
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open the file: {str(e)}")
                '''
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download the file: {str(e)}")
        else:
            messagebox.showerror("Error", f"'{source_path}' does not exist.")

    def logout_function(self,master):
        """Handles logout logic by resetting the screen and showing the login window again."""
        #master.destroy()  # Close the main screen
        self.main_window(master)  # Reopen login window

    def designMainScreen(self,master, username, category):
        """
        Function to design the main screen of the Inward Logistic Handling application.

        This function initializes and positions UI elements such as labels, buttons, and event bindings
        to allow users to perform actions such as data entry, searching, downloading, logging out, and exiting.

        Parameters:
        master (Tk): The root window where the UI elements will be placed.
        username (str): The username of the logged-in user.
        category (str): The role of the user (e.g., "Admin", "User"), which affects button visibility.

        Returns:
        None
        """

        # Restore and focus the main application window
        master.deiconify()  # Ensure the window is not minimized
        master.lift()  # Bring the window to the front
        master.focus_force()  # Set focus to the main window

        # Debugging output to confirm username
        print("User name:", username)

        # Create a label for the application title
        labelFrame = Label(master, text="Inward Logistic Handling", justify=CENTER,
                           font=XXL_FONT, fg='black')

        # Create and configure the "Inward Entry" button
        # This button opens the data entry window
        result_btnAddQuestion = partial(self.data_entry_window, master)
        btn_addQues = Button(master, text="Inward Entry", fg="Black", command=result_btnAddQuestion,
                             font=XL_FONT, width=20, state=NORMAL, bg='RosyBrown1')

        # Create and configure the "Search" button
        # This button opens the search window
        result_createPaper = partial(self.search_window, master)
        btn_createPaper = Button(master, text="Search", fg="Black", command=result_createPaper,
                                 font=XL_FONT, width=20, state=NORMAL, bg='RosyBrown1')

        # Create and configure the "Download" button
        # This button allows users to download the inward register
        result_downloadmaster =  partial(self.download_inward_register,"master")
        btn_usrCtrl = Button(master, text="Download", fg="Black", command=result_downloadmaster,
                             font=XL_FONT, width=20, state=NORMAL, bg='RosyBrown1')

        # Initialize btn_settings as None; only used if the user is an Admin
        btn_settings = None

        if category == "Admin":
            # Create and configure the "Settings" button for Admin users only
            btn_settings = Button(master, text="Settings", fg="Black", command=lambda:self.settings_window(master),
                                  font=XL_FONT, width=20, state=NORMAL, bg='RosyBrown1')

        # Create and configure the "Logout" button
        # This button calls the logout function and hides the main window
        btn_logout = Button(master, text="Logout", fg="Black", command=lambda: self.logout_function(master),
                            font=XL_FONT, width=20, state=NORMAL, bg='RosyBrown1')

        # Create and configure the "Exit" button
        # This button terminates the application
        btn_exit = Button(master, text="Exit", fg="Black", command=master.destroy,
                          font=XL_FONT, width=20, state=NORMAL, bg='RosyBrown1')

        # Position the buttons on the screen using absolute placement
        btn_addQues.place(x=65, y=220)  # Position "Inward Entry" button
        btn_createPaper.place(x=65, y=275)  # Position "Search" button
        btn_usrCtrl.place(x=65, y=330)  # Position "Download" button

        if btn_settings:  # If the user is an Admin, include the "Settings" button
            btn_settings.place(x=65, y=385)  # Position "Settings" below "Download"
            btn_logout.place(x=65, y=440)  # Position "Logout" below "Settings"
            btn_exit.place(x=65, y=495)  # Position "Exit" below "Logout"

        else:  # If the user is not an Admin, exclude "Settings" and adjust button placement
            btn_logout.place(x=65, y=385)  # Position "Logout" below "Download"
            btn_exit.place(x=65, y=440)  # Position "Exit" below "Logout"

        # Bind the 'Escape' key to trigger the Exit button
        master.bind('<Escape>', lambda event=None: btn_exit.invoke())

    def login_window(self,master):
        """
        Function to create and display the login window.

        This function creates a login window using Tkinter's Toplevel,
        allowing users to enter their credentials and authenticate.
        It sets up various UI elements including labels, entry fields,
        buttons, and key bindings for user interactions.

        Parameters:
        master (tk.Tk): The main application window that serves as the parent for the login window.
        """

        # Create a Toplevel window for login, which is a child window of the main application.
        # The 'takefocus=True' ensures that the login window gets focus upon opening.
        login_window = Toplevel(master, takefocus=True)

        # ------------------------- Step 1: Set Window Size and Position ------------------------- #

        # Get screen dimensions dynamically to position the login window at the center
        xSize = master.winfo_screenwidth()
        ySize = master.winfo_screenheight()

        # Set window dimensions and position based on screen size calculations
        # Width = 410, Height = 200
        # The window is positioned at approximately the center of the screen
        login_window.geometry('{}x{}+{}+{}'.format(410, 200, (int(xSize / 2.7)), (int(ySize / 3.8) + 50)))

        # Set the title of the login window
        login_window.title("Account Login")

        # Set background color to white
        login_window.configure(bg="white")

        # Disable the close button functionality
        login_window.protocol('WM_DELETE_WINDOW')

        # Change the background color to 'wheat' for a softer appearance
        login_window.configure(background='wheat')

        # ------------------------- Step 2: Create the Upper Frame ------------------------- #

        # Create an upper frame that contains the login title label
        upperFrame = Frame(login_window, width=300, height=200, bd=8, relief='ridge', bg="white")
        upperFrame.grid(row=1, column=0, padx=20, pady=5, columnspan=2)

        # Label to display login title inside the upper frame
        labelLogin = Label(upperFrame, text="System Authentication", width=30, anchor=CENTER, justify=CENTER,
                           font=('arial narrow', 18, 'normal'), fg='blue', bg='light cyan')
        labelLogin.grid(row=0, column=0, padx=1, pady=1)

        # ------------------------- Step 3: Create the Lower Frame ------------------------- #

        # Create a lower frame to hold the user input fields (Username & Password)
        lowerFrame = Frame(login_window, width=300, height=110, bd=8, relief='ridge', bg="white")
        lowerFrame.grid(row=2, column=0, padx=20, pady=5)

        # ------------------------- Step 4: Username Entry Field ------------------------- #

        # Label for the "User Name" field
        userNameLabel = Label(lowerFrame, text="User Name", width=12, anchor=W, justify=LEFT,
                              font=('arial narrow', 15, 'normal'), bg="white", bd=2, relief='ridge')
        userNameLabel.grid(row=2, column=0)

        # Entry field for the username input
        userNameText = Entry(lowerFrame, width=22, font=('Yu Gothic', 12, 'normal'), bd=2, relief='ridge',
                             bg='light yellow')
        userNameText.grid(row=2, column=1, padx=5)

        # Set the cursor focus on the username field when the window opens
        userNameText.focus_set()

        # ------------------------- Step 5: Password Entry Field ------------------------- #

        # Label for the "Password" field
        passwordLabel = Label(lowerFrame, text="Password", width=12, anchor=W, justify=LEFT,
                              font=('arial narrow', 15, 'normal'), bg="white", bd=2, relief='ridge')
        passwordLabel.grid(row=3, column=0, pady=2)

        # Entry field for password input (masked with '*')
        passwordText = Entry(lowerFrame, width=22, show='*', font=('Yu Gothic', 12, 'normal'), bd=2, relief='ridge',
                             bg='light yellow')
        passwordText.grid(row=3, column=1, padx=5, pady=2)

        # ------------------------- Step 6: Button Frame (Login, Reset, Close) ------------------------- #

        # Create a frame to hold the buttons
        buttonFrame = Frame(login_window, width=200, height=100, bd=4, relief='ridge')
        buttonFrame.grid(row=4, column=0)

        # Partial function to pass parameters to validateStaffLogin when Login button is clicked
        login_result = partial(self.validateStaffLogin, master, userNameText, passwordText, labelLogin, login_window)

        # Login button - Triggers the authentication process
        submit = Button(buttonFrame, text="Login", fg="Black", command=login_result,
                        font=NORM_FONT, width=8, bg='light cyan', highlightcolor="snow")
        submit.grid(row=0, column=0)

        # Reset button - Currently not functional (Needs a function to be assigned)
        clear = Button(buttonFrame, text="Reset", fg="Black", command=None,
                       font=NORM_FONT, width=8, bg='light cyan', underline=0, highlightcolor="black")
        clear.grid(row=0, column=1)

        # Close button - Closes the main application window
        cancel = Button(buttonFrame, text="Close", fg="Black", command=master.destroy,
                        font=NORM_FONT, width=8, bg='light cyan', underline=0, highlightcolor="black")
        cancel.grid(row=0, column=2)

        # ------------------------- Step 7: Keyboard Shortcuts ------------------------- #

        # Pressing "Enter" key triggers the Login button
        login_window.bind('<Return>', lambda event=None: submit.invoke())

        # Pressing "Alt+C" key triggers the Close button
        login_window.bind('<Alt-c>', lambda event=None: cancel.invoke())

        # Pressing "Alt+R" key triggers the Reset button
        login_window.bind('<Alt-r>', lambda event=None: clear.invoke())

        # ------------------------- Step 8: Window Properties ------------------------- #

        # Bring the login window to the front
        login_window.lift()

        # Set focus to the login window to prevent background interactions
        login_window.focus_set()

        # Disable interactions with other windows until login is complete
        login_window.grab_set()

        # Ensure the login window stays on top of all other windows
        login_window.attributes('-topmost', 1)

    def validateStaffLogin(self,master, userNameText, passwordText, labelLogin, login_window):
        """
        Function to validate staff login credentials.

        This function checks if the entered username and password match any records
        in the "Users.xlsx" file. If valid, it proceeds to the main application screen;
        otherwise, it displays a login failure message and resets the login form.

        Parameters:
        master (tk.Tk or tk.Toplevel): The main application window.
        userNameText (tk.Entry): The entry widget containing the username input.
        passwordText (tk.Entry): The entry widget containing the password input.
        labelLogin (tk.Label): The label used to display login status messages.
        login_window (tk.Toplevel): The login window, which will be closed upon successful login.
        """

        # Define the file path of the Excel sheet containing user credentials
        file_path = "Users.xlsx"

        # Initialize login validation flag as False
        bLoginValid = False

        # Variable to store the user's category (e.g., "User" or "Admin")
        category = None

        # ------------------------- Step 1: Check if the Users.xlsx file exists ------------------------- #

        # Verify if the user credentials file exists before attempting to read it
        if os.path.exists(file_path):

            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(file_path)

            # Consider only the necessary columns: 'Username', 'Password', and 'Category'
            df = df[['Username', 'Password', 'Category']]

            # ------------------------- Step 2: Validate User Credentials ------------------------- #

            # Iterate through each row of the DataFrame to check for a matching username and password
            for index, row in df.iterrows():

                # Check if the entered username and password match any record in the file
                if row['Username'] == userNameText.get().strip() and row['Password'] == passwordText.get().strip():
                    bLoginValid = True  # Mark login as valid
                    category = row['Category']  # Store the user's category (e.g., "User" or "Admin")
                    break  # Exit loop as soon as a valid match is found

        # ------------------------- Step 3: Handle Login Success or Failure ------------------------- #

        # If login is valid and the user belongs to an allowed category
        if bLoginValid and category in ["User", "Admin"]:

            # Update the login label to indicate success
            labelLogin.configure(fg='green')
            labelLogin['text'] = "Login Success!!"

            # Print authentication success message to console
            print("Authentication Success for user:", userNameText.get())

            # Retrieve the username from the input field
            un = userNameText.get()

            # Close the login window
            login_window.destroy()

            # Redirect to the main application screen, passing the username and category
            self.designMainScreen(master, un, category)

        else:
            # Update the login label to indicate failure
            labelLogin.configure(fg='red')
            labelLogin['text'] = "Login Failed !! Try Again"

            # Clear the login form to reset the fields
            self.clear_loginForm(userNameText, passwordText)

            # Set focus back to the password field for easy re-entry
            passwordText.focus()

    def clear_loginForm(self,userNameText, passwordText):
        """
        Function to clear the login form fields.

        This function resets the username and password entry fields by:
        - Deleting any existing text in both fields.
        - Changing their text color to black.
        - Setting the cursor focus back to the username field.

        Parameters:
        userNameText (tk.Entry): The entry widget for the username.
        passwordText (tk.Entry): The entry widget for the password.
        """

        # Clear any text in the username entry field
        userNameText.delete(0, END)

        # Reset the text color of the username field to black
        userNameText.configure(fg='black')

        # Clear any text in the password entry field
        passwordText.delete(0, END)

        # Reset the text color of the password field to black
        passwordText.configure(fg='black')

        # Set the focus back to the username entry field for user convenience
        userNameText.focus_set()

    # set up the root window
    def main_window(self,root):
        """
        Function to create and display the main application window.

        This function initializes a Tkinter root window, sets its title, size,
        and background color, then sets up a canvas to display a background image.
        It also initializes the database and calls the login window function
        before starting the Tkinter main event loop.
        """


        # Set the title of the window
        root.title("Inward Logistic Maintenance")

        # Get the screen width and height using pyautogui
        width, height = pyautogui.size()

        # Define the geometry of the window dynamically based on screen size
        # Window width is set to 1.35 times smaller than the screen width
        # Window height is set to 1.25 times smaller than the screen height
        # Window is positioned at 1/9 of screen width from the left and 1/12 from the top
        root.geometry('{}x{}+{}+{}'.format(
            int(width / 1.35), int(height / 1.25), int(width / 9), int(height / 12)
        ))

        # Set the background color of the root window
        root.configure(bg='AntiqueWhite1')

        # ---------------- Setup Canvas for Background Image ---------------- #

        # Get screen dimensions again to set up a full-size canvas
        canvas_width, canvas_height = pyautogui.size()

        # Create a Canvas widget with the full screen dimensions
        canvas = Canvas(root, width=canvas_width, height=canvas_height)

        # Load and resize the background image to twice the screen size for better resolution
        myimage = ImageTk.PhotoImage(
            Image.open("..\\image\\3-4.jpg").resize((canvas_width * 2, canvas_height * 2))
        )

        # Place the image at the top-left corner of the canvas (0,0) with 'nw' (northwest) anchor
        canvas.create_image(0, 0, anchor="nw", image=myimage)

        # Pack the canvas into the root window to make it visible
        canvas.pack()

        # ---------------- Initialize Database and Launch Login Window ---------------- #

        # Call the function to initialize the database (assumed to be defined elsewhere)
        self.initialize_database()

        # Call the function to display the login window, passing the root window as a parameter
        self.login_window(root)

        # Start the Tkinter event loop to keep the GUI running
        root.mainloop()

# Create the root window for the GUI
root = tk.Tk()
logistics_obj = Logistics(root)


