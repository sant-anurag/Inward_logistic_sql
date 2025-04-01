from common_utils import *

class EditWindow:
    def __init__(self, master, download_callback):
        """
        Initializes the edit window for filtering and displaying data from an Excel file.

        :param master: The parent Tkinter window or frame where the edit window will be attached.
        :param download_callback: A function to handle downloading the filtered data.
        """
        self.view_edit_window = None
        self.tree = None
        self.table_frame = None
        self.edit_window = None
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
        self.fields = column_names

        # Call method to create and display the edit window
        self.create_edit_window()

    def create_edit_window(self):
        """
        Creates and configures the edit window where users can filter data from an Excel file.

        This method initializes a new top-level Tkinter window, sets its dimensions dynamically based on screen size,
        and organizes UI elements including filter fields, buttons, and a table for displaying results.
        """
        # Create a new top-level window for the edit interface
        self.edit_window = tk.Toplevel(self.master)

        # Get screen width and height for dynamic positioning of the window
        width, height = pyautogui.size()

        # Set window title
        self.edit_window.title("Search")

        # Set window dimensions (600x500) and position it roughly in the center of the screen
        self.edit_window.geometry(f'600x400+{int(width / 3.2)}+{int(height / 4)}')

        # Set background color
        self.edit_window.configure(background='wheat')

        # Disable resizing of the edit window
        self.edit_window.resizable(width=False, height=False)

        # Create UI frames to organize different sections of the window
        self.heading_frame = tk.Frame(self.edit_window, bg='wheat')  # Header section
        self.filter_frame = tk.Frame(self.edit_window, bd=4, relief='ridge', bg='wheat')  # Filter fields section
        self.button_frame = tk.Frame(self.edit_window, bd=4, relief='ridge', bg='wheat')  # Buttons section
        self.table_frame = tk.Frame(self.edit_window, bd=4, relief='ridge', bg='wheat')  # Table display section

        # Create and pack the heading label inside the heading frame
        heading = tk.Label(self.heading_frame, text="Search", font=('ariel narrow', 15, 'bold'), bg='wheat')
        heading.pack()

        # Add an initial filter row where users can specify filter criteria
        self.add_filter_row()

        # Create a status label to display messages (e.g., number of records found)
        self.status_label = tk.Label(self.edit_window, text="Select Filter and Press Search",
                                     font=('ariel narrow', 12, 'bold'), bg='wheat', fg='green', width=50)

        # Call a method to create buttons (Search, Add Filter, Download, Close)
        self.create_buttons()

        # Pack (place) the frames in the edit window
        self.heading_frame.pack()  # Header
        self.filter_frame.pack(padx=10, pady=10, fill=tk.X)  # Filter section
        self.button_frame.pack(pady=10)  # Buttons section
        self.status_label.pack(pady=5)  # Status label
        self.create_search_tree()

    def create_buttons(self):
        """
        Creates and adds buttons to the button frame, providing functionality for editing data,
        downloading filtered results, and closing the edit window.
        """
        # Button to execute the edit based on selected filters
        edit_button = tk.Button(self.button_frame, text="Search", command=self.search_data,
                                font=('ariel narrow', 10), width=10, bg='light cyan')
        edit_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Bind "Enter" key to trigger the edit button
        self.edit_window.bind("<Return>", lambda event: self.search_data())

        # Button to download the filtered data; calls the download callback function
        result_download = partial(self.download_filteredData)
        self.download_button = tk.Button(self.button_frame, text="Download",
                                         command=result_download,
                                         font=('ariel narrow', 10), width=10, bg='lightgrey',
                                         disabledforeground="darkgrey", state=DISABLED)
        self.download_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Bind "Alt" + "D" to trigger the download
        self.edit_window.bind("<Alt-Key-d>", lambda event: result_download())

        # Button to close the edit window
        close_button = tk.Button(self.button_frame, text="Close", command=self.edit_window.destroy,
                                 font=('ariel narrow', 10), width=10, bg='light cyan')
        close_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Bind "Escape" key to close the window
        self.edit_window.bind("<Escape>", lambda event: self.edit_window.destroy())
        
    def create_search_tree(self):
        # Define columns for the table
        columns = database_fields_load

        self.tree = ttk.Treeview(self.edit_window, columns=columns, show="headings", height=5)
        # Create a style for the treeview heading with light cyan background
        style = ttk.Style()
        style.configure("Treeview.Heading", background="light cyan", font=("Arial", 10, "bold"), anchor="center")
        self.tree.bind("<Double-1>", self.view_edit_record)  # Double-click to open View/Edit window

        # Define column headings and set their properties
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            if col == 1 or col == 2:
                self.tree.column(col, width=60, anchor="center")
            else:
                self.tree.column(col, width=100, anchor="center")

        # Add scrollbars
        v_scroll = ttk.Scrollbar(self.edit_window, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(self.edit_window, orient="horizontal", command=self.tree.xview)

        # Configure the Treeview to use the scrollbars
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Place tree and scrollbars

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both")

        self.edit_window.focus()  # Focus on the new window
        self.edit_window.grab_set()  # Make the window model

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
        #self.update_window_size("extend")

    def search_data(self):
        try:
            # Connect to the database
            connection = mysql.connector.connect(**serverdb_config)
            cursor = connection.cursor()

            # Base query
            query = "SELECT * FROM inward_logistic WHERE 1=1"
            print("Initial query:", query)

            # Build the query based on filters
            for column_var, operator_option, entry_var, _ in self.filter_rows:
                column = column_var.get()
                operator = operator_option.get()
                value = entry_var.get().strip()
                print("Column:", column, "operator:", operator, "value:", value)
                if column and operator and value:
                    column = f"`{column}`"  # Enclose column name in backticks
                    if operator == "Equals":
                        query += f" AND {column} = '{value}'"
                    elif operator == "Not Equals":
                        query += f" AND {column} != '{value}'"
                    elif operator == "Contains":
                        query += f" AND {column} LIKE '%{value}%'"
                    elif operator == "Not Contains":
                        query += f" AND {column} NOT LIKE '%{value}%'"

            # Execute the query
            print("Final query:", query)
            cursor.execute(query)
            rows = cursor.fetchall()

            # Get column names
            columns = [desc[0] for desc in cursor.description]

            # Clear existing tree view data
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert new data into tree view
            for row in rows:
                self.tree.insert("", "end", values=row)

            # Display record count
            record_count = len(rows)
            self.status_label.config(
                text=f"{record_count} records found" if record_count else "0 records found",
                fg="green" if record_count else "red"
            )

            # Close the database connection
            cursor.close()
            connection.close()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit the database: {str(e)}")
            
    def view_edit_record(self, event):
        """Opens a new window for viewing and editing a selected record with dropdowns and date pickers."""
        selected_item = self.tree.selection()
        if not selected_item:
            return  # No item selected

        record = self.tree.item(selected_item, "values")[1:]

        # Store the first element in a variable
        serial_no = self.tree.item(selected_item, "values")[0]
        print("Serial no :  ", serial_no)
        if not record:
            return
        width, height = pyautogui.size()
        self.view_edit_window = tk.Toplevel(self.edit_window)
        self.view_edit_window.title("View/Edit Record")
        self.view_edit_window.geometry(f'1050x550+{int(width / 3.2)}+{int(height / 3.5)}')
        self.view_edit_window.configure(background="wheat")

        heading_frame = tk.Frame(self.view_edit_window, bg="wheat")
        heading_frame.pack(fill="x")
        heading = tk.Label(heading_frame, text="View/Edit Record", font=("Arial Narrow", 15, "bold"), bg='wheat')
        heading.pack(pady=10)

        display_frame = tk.Frame(self.view_edit_window, bg="wheat", width=600, height=300, bd=4, relief='ridge')
        display_frame.pack(pady=10)

        button_frame = tk.Frame(self.view_edit_window, bg="wheat",width=200, height=100, bd=4, relief='ridge')
        button_frame.pack(pady=10)

        fields = database_fields

        self.view_edit_entries = []
        dropdown_fields = {"Return Type": ["Non-Returnable", "Returnable"], "Benefit Type": ["Non-Benefit", "Benefit", "None"]}

        num_fields = len(fields)
        for i, field in enumerate(fields):
            row, col = divmod(i, 2)  # Distribute fields into two columns

            label = tk.Label(display_frame, text=field, width=20, anchor=tk.W, font=("Bookman Old Style", 10), bg="wheat")
            label.grid(row=row, column=col * 2, padx=5, pady=5, sticky="w")
            style = ttk.Style()
            style.configure("Readonly.TEntry", background="light grey")

            if field in dropdown_fields:
                var = tk.StringVar(value=record[i])
                dropdown = ttk.Combobox(display_frame, values=dropdown_fields[field], textvariable=var,
                                        state="disabled",width=38,font=("Bookman Old Style", 10))
                dropdown.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
                self.view_edit_entries.append((field, var, dropdown))
            elif field == "Date":
                date_var = tk.StringVar(value=record[i])
                date_entry = DateEntry(display_frame, textvariable=date_var, state="disabled",width=38,font=("Bookman Old Style", 10))
                date_entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
                self.view_edit_entries.append((field, date_var, date_entry))
            else:

                entry = tk.Entry(display_frame, width=40, font=("Bookman Old Style", 10),readonlybackground="light grey")
                entry.insert(0, record[i])
                entry.config(state="disabled")
                entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
                self.view_edit_entries.append((field, entry))

        def enable_edit():
            # Update the Treeview
            self.save_button_edit.update_idletasks()
            self.save_button_edit.configure(state=ACTIVE,bg='light cyan')
            for item in self.view_edit_entries:
                if isinstance(item[1], tk.StringVar):
                    item[2].config(state="readonly")
                else:
                    item[1].config(state="normal", bg="snow")

        def save_changes():
            updated_record = [item[1].get() for item in self.view_edit_entries]
            print("Updated record count:", len(updated_record))

            # Connect to the database
            connection = mysql.connector.connect(**serverdb_config)
            cursor = connection.cursor()

            # SQL query to update the record
            update_query = """
            UPDATE inward_logistic
            SET Inward_No = %s,Return_Type = %s, Benefit_Type = %s, Date = %s, Time = %s, Gate_Entry_No = %s, Invoice_No = %s, PO_No = %s, BOE_No = %s, 
                Return_Date = %s, Return_Time = %s, Supplier = %s, Material = %s, Qty = %s, Department = %s, Project = %s, 
                TPL_Name = %s, Vehicle = %s, Received = %s, Authorized = %s, Security = %s, Remark = %s, TPL_Remarks = %s
            WHERE id = %s
            """

            # Execute the update query
            cursor.execute(update_query, (*updated_record, serial_no))
            connection.commit()

            # Close the database connection
            cursor.close()
            connection.close()

            # Update the Treeview and show success message
            self.tree.item(selected_item, values=updated_record)
            messagebox.showinfo("Success", "Record edited successfully and saved !!!", parent=self.view_edit_window)
            #self.load_last_entries()

        edit_button = tk.Button(button_frame, text="Edit", command=enable_edit, bg="light cyan",font=('ariel narrow', 10), width=10)
        edit_button.pack(side="left", padx=5)
        self.save_button_edit = tk.Button(button_frame, text="Save", command=save_changes, bg="grey",font=('ariel narrow', 10), width=10,state=DISABLED)
        self.save_button_edit.pack(side="left", padx=5)
        close_button = tk.Button(button_frame, text="Close", command=self.view_edit_window.destroy, bg="light cyan",font=('ariel narrow', 10), width=10)
        close_button.pack(side="left", padx=5)

        self.view_edit_window.focus()

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

