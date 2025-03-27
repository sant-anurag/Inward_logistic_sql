from common_utils import *

class SearchWindow:
    def __init__(self, master, download_callback):
        """
        Initializes the search window for filtering and displaying data from an Excel file.

        :param master: The parent Tkinter window or frame where the search window will be attached.
        :param download_callback: A function to handle downloading the filtered data.
        """
        self.table_frame = None
        self.search_window = None
        self.button_frame = None
        self.filter_frame = None
        self.heading_frame = None
        self.remove_button = None
        self.download_button = None
        self.master = master  # Store the parent window reference
        self.download_callback = download_callback  # Store the download callback function

        # List to store dynamically created filter rows (each containing column selection, operator, and value entry)
        self.filter_rows = []

        # Define the available fields (columns) in the dataset that users can filter by
        self.fields = database_fields

        # Define the file path of the source Excel file containing data
        self.file_name = os.path.join(
            os.path.join(os.environ["USERPROFILE"], "OneDrive - FORVIA"),
            "Inward_logistic_master", "Inward Material Register.xlsx"
        )

        # Define the file path where the filtered data will be saved
        self.output_filename = os.path.join(
            os.path.join(os.environ["USERPROFILE"], "OneDrive - FORVIA"),
            "Inward_logistic_master", "Filtered_Inward_Material.xlsx"
        )

        # Call method to create and display the search window
        self.create_search_window()

    def create_search_window(self):
        """
        Creates and configures the search window where users can filter data from an Excel file.

        This method initializes a new top-level Tkinter window, sets its dimensions dynamically based on screen size,
        and organizes UI elements including filter fields, buttons, and a table for displaying results.
        """
        # Create a new top-level window for the search interface
        self.search_window = tk.Toplevel(self.master)

        # Get screen width and height for dynamic positioning of the window
        width, height = pyautogui.size()

        # Set window title
        self.search_window.title("Search")

        # Set window dimensions (600x500) and position it roughly in the center of the screen
        self.search_window.geometry(f'600x200+{int(width / 3.2)}+{int(height / 3)}')

        # Set background color
        self.search_window.configure(background='wheat')

        # Disable resizing of the search window
        self.search_window.resizable(width=False, height=False)

        # Create UI frames to organize different sections of the window
        self.heading_frame = tk.Frame(self.search_window, bg='wheat')  # Header section
        self.filter_frame = tk.Frame(self.search_window, bd=4, relief='ridge', bg='wheat')  # Filter fields section
        self.button_frame = tk.Frame(self.search_window, bd=4, relief='ridge', bg='wheat')  # Buttons section
        self.table_frame = tk.Frame(self.search_window, bd=4, relief='ridge', bg='wheat')  # Table display section

        # Create and pack the heading label inside the heading frame
        heading = tk.Label(self.heading_frame, text="Search", font=('ariel narrow', 15, 'bold'), bg='wheat')
        heading.pack()

        # Add an initial filter row where users can specify filter criteria
        self.add_filter_row()

        # Create a status label to display messages (e.g., number of records found)
        self.status_label = tk.Label(self.search_window, text="Select Filter and Press Search",
                                     font=('ariel narrow', 12, 'bold'), bg='wheat', fg='green', width=50)

        # Call a method to create buttons (Search, Add Filter, Download, Close)
        self.create_buttons()

        # Pack (place) the frames in the search window
        self.heading_frame.pack()  # Header
        self.filter_frame.pack(padx=10, pady=10, fill=tk.X)  # Filter section
        self.button_frame.pack(pady=10)  # Buttons section
        self.status_label.pack(pady=5)  # Status label

    def add_filter_row(self):
        """
        Adds a new filter row to the filter section of the search window.

        Each filter row consists of:
        - A dropdown to select the column to filter.
        - A dropdown to choose the filtering operator (Equals, Not Equals, Contains, Not Contains).
        - A text entry field where the user inputs the value to filter by.
        """
        # Create a frame to hold the filter row components
        filter_row = tk.Frame(self.filter_frame, bg='wheat')
        filter_row.pack(pady=5, padx=10, fill=tk.X,expand=True)

        # Create and pack the label for the column selection dropdown
        tk.Label(filter_row, text="Column", font=('ariel narrow', 10), bg='wheat').pack(side=tk.LEFT, padx=5)

        # Create a dropdown for selecting a column from the available fields
        column_var = tk.StringVar()
        column_option = ttk.Combobox(filter_row, textvariable=column_var, values=self.fields, width=20,
                                     state='readonly')
        column_option.pack(side=tk.LEFT, padx=5)

        # Create and pack the label for the operator selection dropdown
        tk.Label(filter_row, text="Operator", font=('ariel narrow', 10), bg='wheat').pack(side=tk.LEFT, padx=5)

        # Create a dropdown for selecting an operator (equality, containment, etc.)
        operator_option = ttk.Combobox(filter_row, values=["Equals", "Not Equals", "Contains", "Not Contains"],
                                       width=10, state='readonly')
        operator_option.pack(side=tk.LEFT, padx=5)

        # Create a text entry field for entering the filter value
        entry_var = tk.StringVar()
        entry = tk.Entry(filter_row, textvariable=entry_var, width=20, font=('ariel narrow', 10), bg='light yellow')
        entry.pack(side=tk.LEFT, padx=5)

        # Store the filter row components for future reference
        self.filter_rows.append((column_var, operator_option, entry_var, filter_row))
        if len(self.filter_rows) > 1:
            self.remove_button.configure(bg='light cyan', highlightbackground='light cyan', fg='black',
                                           state=ACTIVE)

            # Modify window geometry to expand by 15 pixels in height
        self.update_window_size("extend")

    def update_window_size(self,update_type):
        """
        Expands/Shrinks the search window by 30 pixels in height.
        """
        print("Calling update_window_size , and requesting :  ",update_type)
        self.search_window.update_idletasks()  # Ensure the window is updated before getting its size
        if update_type == "extend":
            width, height, x, y = map(int,
                                      self.search_window.geometry().split('+')[0].split('x') + self.search_window.geometry().split(
                                          '+')[1:])
            new_height = height + 30  # Increase height by 30 pixels
            self.search_window.geometry(f"{width}x{new_height}+{x}+{y}")  # Apply new geometry
        elif update_type == "shrink":
            width, height, x, y = map(int,
                                      self.search_window.geometry().split('+')[0].split('x') + self.search_window.geometry().split(
                                          '+')[1:])
            new_height = height - 30  # Increase height by 30 pixels
            self.search_window.geometry(f"{width}x{new_height}+{x}+{y}")  # Apply new geometry
        else:
            donothing()
        self.search_window.update_idletasks()  # Ensure the window is updated before getting its size

    def remove_filter_row(self):
        """
        Removes the last added filter row, if any, and updates the search criteria.
        Ensures that the first row is never deleted and disables the remove button when only one row remains.
        """
        if len(self.filter_rows) > 1:  # Ensure at least one row remains
            last_row = self.filter_rows.pop()  # Remove the last added filter row
            for widget in last_row:
                if isinstance(widget, tk.Widget):  # Destroy only Tkinter widget objects
                    widget.destroy()

            # If only one row remains after deletion, disable the "-" button
            if len(self.filter_rows) == 1:
                self.remove_button.configure(bg='lightgrey', disabledforeground="darkgrey", state=DISABLED)
        self.update_window_size("shrink")

    def download_filteredData(self):
        source_path = self.output_filename

        print("download_filteredData-> ", source_path)

        # Get user's default download directory
        download_dir = str(Path.home() / "Downloads")
        destination_path = os.path.join(download_dir, "Filtered_Inward_Material.xlsx")

        if os.path.exists(source_path):
            try:
                shutil.copy(source_path, destination_path)
                self.status_label.config(text="Success ,please check ""Downloads"" folder!!!", fg="green")
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

    def create_buttons(self):
        """
        Creates and adds buttons to the button frame, providing functionality for adding filters, searching data,
        downloading filtered results, and closing the search window.
        """
        # Button to add a filter row dynamically
        add_button = tk.Button(self.button_frame, text="+", command=self.add_filter_row,
                               font=('ariel narrow', 10), width=10, bg='light cyan')
        add_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.remove_button = tk.Button(self.button_frame, text="-", command=self.remove_filter_row,
                               font=('ariel narrow', 10), width=10, bg='lightgrey', disabledforeground="darkgrey",state = DISABLED)
        self.remove_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Button to execute the search based on selected filters
        search_button = tk.Button(self.button_frame, text="Search", command=self.search_data,
                                  font=('ariel narrow', 10), width=10, bg='light cyan')
        search_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Bind "Enter" key to trigger the search button
        self.search_window.bind("<Return>", lambda event: self.search_data())

        # Bind "Alt" + "+" to add a filter row
        self.search_window.bind("<Alt-Key-plus>", lambda event: self.add_filter_row())

        # Bind "Alt" + "-" to remove a filter row
        self.search_window.bind("<Alt-Key-minus>", lambda event: self.remove_filter_row())

        # Button to download the filtered data; calls the download callback function
        result_download  = partial(self.download_filteredData)
        self.download_button = tk.Button(self.button_frame, text="Download",
                                    command=result_download,
                                    font=('ariel narrow', 10), width=10, bg='lightgrey', disabledforeground="darkgrey",state = DISABLED)
        self.download_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Bind "Alt" + "D" to trigger the download
        self.search_window.bind("<Alt-Key-d>", lambda event: result_download())

        # Button to close the search window
        close_button = tk.Button(self.button_frame, text="Close", command=self.search_window.destroy,
                                 font=('ariel narrow', 10), width=10, bg='light cyan')
        close_button.pack(side=tk.LEFT, padx=10, pady=5)
        # Bind "Escape" key to close the window
        self.search_window.bind("<Escape>", lambda event: self.search_window.destroy())

    def search_data(self):
        try:
            df = pd.read_excel(self.file_name, dtype=str)  # Read everything as string initially
        except Exception as e:
            print("Error loading Excel file:", e)
            return

        for column_var, operator_option, entry_var, _ in self.filter_rows:
            column = column_var.get()
            operator = operator_option.get()
            value = entry_var.get().strip()

            if column and operator and value:
                try:
                    # Check if the column contains numeric data
                    if df[column].str.replace('.', '', 1).str.isdigit().all():
                        df[column] = pd.to_numeric(df[column],
                                                   errors='coerce')  # Convert column back to numeric if applicable
                        value = pd.to_numeric(value, errors='coerce')  # Convert input value to number if possible

                    # Apply filters based on the selected operator
                    if operator == "Equals":
                        df = df[df[column] == value]
                    elif operator == "Not Equals":
                        df = df[df[column] != value]
                    elif operator == "Contains":
                        safe_value = re.escape(value)  # Escape special characters
                        df = df[df[column].str.contains(safe_value, na=False, regex=True)]
                    elif operator == "Not Contains":
                        safe_value = re.escape(value)
                        df = df[~df[column].str.contains(safe_value, na=False, regex=True)]
                except Exception as e:
                    print(f"Error during filtering: {e}")
                    continue

        # Display record count and save results
        record_count = len(df)
        self.status_label.config(
            text=f"{record_count} records found, Use 'Download' for viewing search results" if record_count else "0 records found",
            fg="green" if record_count else "red"
        )

        df.to_excel(self.output_filename, index=False)

        # Load the Excel file for formatting
        wb = load_workbook(self.output_filename)
        ws = wb.active

        # Define header styling
        header_fill = PatternFill(start_color="D9FFFF", end_color="D9FFFF", fill_type="lightUp")  # Light cyan
        header_font = Font(name="Bookman Old Style", size=11, bold=True)  # Bold font for headers
        header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)  # Center align

        # Apply styles to header row
        for col_num, col_name in enumerate(df.columns, start=1):
            col_letter = get_column_letter(col_num)
            cell = ws[f"{col_letter}1"]  # Get header cell
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center",
                                       wrap_text=False)  # 🔥 Disable wrap for headers

            # Adjust column width based on column name length
            ws.column_dimensions[col_letter].width = len(col_name) + 5  # Increase slightly for better fit

        # Apply font style, adjust column width, and wrap text for data rows
        for col_num, col_cells in enumerate(ws.columns, start=1):
            max_length = max((len(str(cell.value or "")) for cell in col_cells[1:]), default=0)  # Handle empty columns
            col_letter = get_column_letter(col_num)

            for cell in col_cells[1:]:  # Skip header row
                cell.font = Font(name="Bookman Old Style", size=11)
                cell.alignment = Alignment(vertical="center", wrap_text=len(str(cell.value or "")) > 50)  # Handle None values

            # Adjust column width based on content, capped at 50
            ws.column_dimensions[col_letter].width = min(max(max_length + 5, ws.column_dimensions[col_letter].width), 50)

        wb.save(self.output_filename)

        print(f"Filtered data saved to {self.output_filename}")

        if record_count > 0:
            self.download_button.configure(bg='light cyan', highlightbackground='light cyan', fg='black', state=ACTIVE)
            try:
                os.startfile(self.output_filename)  # Works on Windows
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open the file: {str(e)}")

    def display_filtered_data(self, df):
        # Remove any existing widgets from the table frame to refresh the data display
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Create a container frame inside the table_frame to hold the table components
        container = tk.Frame(self.table_frame)
        container.pack(fill=tk.BOTH, expand=True)  # Allow it to expand and fill available space

        # Create a canvas inside the container to enable scrolling when the data overflows
        canvas = tk.Canvas(container, bg='wheat')

        # Create a vertical scrollbar and link it to the canvas for scrolling functionality
        scrollbar_y = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

        # Create a horizontal scrollbar and link it to the canvas for scrolling functionality
        scrollbar_x = tk.Scrollbar(self.table_frame, orient="horizontal", command=canvas.xview)

        # Create a frame inside the canvas that will hold the actual table content
        scrollable_frame = tk.Frame(canvas, bg="wheat")

        # Bind a function to dynamically update the scroll region when the frame size changes
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Add the scrollable frame inside the canvas window, anchored to the top-left (nw)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Configure the canvas to sync scrolling with the scrollbars
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        # Populate the table only if filtered data count is <= 50
        if len(df) <= 50:
            # Populate the table with column headers
            for col_idx, col_name in enumerate(df.columns):
                tk.Label(scrollable_frame, text=col_name, font=('ariel narrow', 10, 'bold'), bg='wheat') \
                    .grid(row=0, column=col_idx, padx=5, pady=5)  # Place column headers in the first row

            # Populate the table with data rows
                # Populate the table with data rows
                for row_idx, row in df.iterrows():
                    for col_idx, value in enumerate(row):
                        display_value = "NA" if (pd.isna(value) or value is None or value == "") else str(value)
                        tk.Label(scrollable_frame, text=display_value, font=('ariel narrow', 10), bg='wheat') \
                            .grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)

        # Pack the canvas on the left side, allowing it to expand and fill space
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Pack the vertical scrollbar to the right, allowing vertical scrolling
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Pack the horizontal scrollbar at the bottom, allowing horizontal scrolling
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Ensure the table frame itself expands and fills available space in the GUI
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

