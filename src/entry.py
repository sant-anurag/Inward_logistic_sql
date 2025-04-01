from xml.etree.ElementTree import tostring

from common_utils import *

class DataEntryWindow:
    def __init__(self, master):
        """
        Initializes the DataEntryWindow class.

        This constructor takes a Tkinter root window (master) and creates the data entry window.
        The method responsible for creating the data entry interface is called immediately.

        :param master: The parent Tkinter window.
        """
        self.master = master
        self.create_data_entry_window()

    def create_data_entry_window(self):
        """
        Creates a data entry window for recording inward material details.

        The window includes:
        - A heading section
        - A form with various input fields
        - Buttons for saving, resetting, and closing the form
        """

        # Get screen dimensions for centering the window
        width, height = pyautogui.size()
        self.data_entry_window = tk.Toplevel(self.master)
        self.data_entry_window.title("Inward Material Entry")

        # Set window size and position it near the center of the screen
        self.data_entry_window.geometry(f'975x650+{int(width / 3.2)}+{int(height / 3.5)}')
        self.data_entry_window.configure(background='wheat')
        self.data_entry_window.resizable(width=True, height=True)  # Disable window resizing


        # Create main frames for UI organization
        self.heading_frame = tk.Frame(self.data_entry_window, bg='wheat')
        self.data_entry_frame = tk.Frame(self.data_entry_window, width=600, height=450, bd=4, relief='ridge',
                                         bg='wheat')
        self.button_frame = tk.Frame(self.data_entry_window, width=200, height=100, bd=4, relief='ridge', bg='wheat')
        self.data_display_frame = tk.Frame(self.data_entry_window, width=600, height=200, bd=4, relief='ridge',
                                           bg='white')

        # Place frames in the main window
        self.heading_frame.grid(row=0, column=0, columnspan=2)
        self.data_entry_frame.grid(row=1, column=0)
        self.button_frame.grid(row=2, column=0, columnspan=2)
        self.data_display_frame.grid(row=3, column=0, sticky="nsew")

        # Configure the grid to expand
        self.data_entry_window.grid_rowconfigure(3, weight=1)
        self.data_entry_window.grid_columnconfigure(0, weight=1)

        # Heading label
        heading = tk.Label(self.heading_frame, text="Inward Material Entry", font=('ariel narrow', 15, 'bold'),
                           bg='wheat')
        heading.grid(row=0, column=0)

        # List of field names for the form
        fields = database_fields

        self.entry_fields = []  # List to store field input widgets

        # Function to enable/disable return date and time fields
        def toggle_return_fields(*args):
            if returnable_type.get() == "Returnable":
                return_date_entry.configure(state="normal")
                return_time_entry.configure(state="normal")
            else:
                return_date_entry.configure(state="disabled")
                return_time_entry.configure(state="disabled")

        # Loop through fields and create corresponding labels and input fields
        for i, field in enumerate(fields):
            label = tk.Label(self.data_entry_frame, text=field, width=20, anchor=tk.W, justify=tk.LEFT,
                             font=('ariel narrow', 10), bg='wheat')

            # Position labels in two columns for better UI layout
            if i < len(fields) // 2 or field == "TPL Remarks":
                if field == "TPL Remarks":
                    label.grid(row=len(fields) // 2 , column=0, padx=5, pady=5)
                else:
                    label.grid(row=i, column=0, padx=5, pady=5)
            else:
                label.grid(row=i - len(fields) // 2, column=2, padx=5, pady=5)

            # Create input fields based on the field type
            if field == "Return Type":
                returnable_type = tk.StringVar(self.data_entry_frame, "Non-Returnable")
                returnable_type_option = ttk.Combobox(self.data_entry_frame, textvariable=returnable_type,
                                                      values=("Non-Returnable", "Returnable"), width=44)
                returnable_type_option.grid(row=i if i < len(fields) // 2 else i - len(fields) // 2,
                                            column=1 if i < len(fields) // 2 else 3, padx=5, pady=5)
                self.entry_fields.append(returnable_type)
                # Bind the function to detect changes in "Return Type"
                returnable_type.trace_add("write", toggle_return_fields)

            elif field == "Benefit Type":
                benefit_type = tk.StringVar(self.data_entry_frame, "Non-Benefit")
                benefit_type_option = ttk.Combobox(self.data_entry_frame, textvariable=benefit_type,
                                                   values=("Non-Benefit", "Benefit", "None"), width=44)
                benefit_type_option.grid(row=i if i < len(fields) // 2 else i - len(fields) // 2,
                                         column=1 if i < len(fields) // 2 else 3, padx=5, pady=5)
                self.entry_fields.append(benefit_type)

            elif field == "Date":
                date_entry = DateEntry(self.data_entry_frame, width=44)
                date_entry.grid(row=i if i < len(fields) // 2 else i - len(fields) // 2,
                                column=1 if i < len(fields) // 2 else 3, padx=5, pady=5)
                self.entry_fields.append(date_entry)

            elif field == "Time":
                time_entry = tk.Entry(self.data_entry_frame, width=40, font=('ariel narrow', 10), bg='light yellow')
                time_entry.insert(0, datetime.now().strftime("%H:%M:%S"))
                time_entry.grid(row=i if i < len(fields) // 2 else i - len(fields) // 2,
                                column=1 if i < len(fields) // 2 else 3, padx=5, pady=5)
                self.entry_fields.append(time_entry)

            elif field == "Return Date":
                return_date_entry  = DateEntry(self.data_entry_frame, width=44)
                return_date_entry .grid(row=i if i < len(fields) // 2 else i - len(fields) // 2,
                                column=1 if i < len(fields) // 2 else 3, padx=5, pady=5)
                return_date_entry.configure(state="disabled")  # Initially disabled
                self.entry_fields.append(return_date_entry )

            elif field == "Return Time":
                return_time_entry = tk.Entry(self.data_entry_frame, width=40, font=('ariel narrow', 10), bg='light yellow')
                return_time_entry.insert(0, datetime.now().strftime("%H:%M:%S"))
                return_time_entry.grid(row=i if i < len(fields) // 2 else i - len(fields) // 2,
                                column=1 if i < len(fields) // 2 else 3, padx=5, pady=5)
                return_time_entry.configure(state="disabled")  # Initially disabled
                self.entry_fields.append(return_time_entry)

            elif field == "TPL Remarks":
                tplremark_entry = tk.Text(self.data_entry_frame, width=40, height=3, font=('ariel narrow', 10),
                                       bg='light yellow')
                tplremark_entry.grid(row=i - len(fields) // 2, column=1, rowspan=3, padx=5, pady=5)
                self.entry_fields.append(tplremark_entry)

            elif field == "Remark":
                remark_entry = tk.Text(self.data_entry_frame, width=40, height=5, font=('ariel narrow', 10),
                                       bg='light yellow')
                remark_entry.grid(row=i if i < len(fields) // 2 else i - len(fields) // 2,
                           column=1 if i < len(fields) // 2 else 3,  rowspan=3,padx=5, pady=5)
                self.entry_fields.append(remark_entry)

            elif field == "Project_Name":
                project_names = get_project_names()
                project_dropdown = ttk.Combobox(self.data_entry_frame, values=project_names, font=('ariel narrow', 10),
                                                width=37)
                if project_names:
                    project_dropdown.set(project_names[0])
                project_dropdown.grid(row=i if i < len(fields) // 2 else i - len(fields) // 2,
                                      column=1 if i < len(fields) // 2 else 3, padx=5, pady=5)
                self.entry_fields.append(project_dropdown)

            else:
                entry = tk.Entry(self.data_entry_frame, width=40, font=('ariel narrow', 10), bg='light yellow')
                entry.grid(row=i if i < len(fields) // 2 else i - len(fields) // 2,
                           column=1 if i < len(fields) // 2 else 3, padx=5, pady=5)
                self.entry_fields.append(entry)

        # Buttons for form actions
        save_button = tk.Button(self.button_frame, text="Save", fg="Black", command=self.save_data,
                                font=('ariel narrow', 10), width=10, bg='light cyan')
        reset_button = tk.Button(self.button_frame, text="Reset", fg="Black", command=self.reset_fields,
                                 font=('ariel narrow', 10), width=10, bg='light cyan')
        close_button = tk.Button(self.button_frame, text="Close", fg="Black", command=self.data_entry_window.destroy,
                                 font=('ariel narrow', 10), width=10, bg='light cyan')

        # Arrange buttons in the button frame
        save_button.grid(row=0, column=0, padx=5, pady=5)
        reset_button.grid(row=0, column=1, padx=5, pady=5)
        close_button.grid(row=0, column=2, padx=5, pady=5)

        # Define columns for the table
        columns = database_fields_load

        self.tree = ttk.Treeview(self.data_display_frame, columns=columns, show="headings", height=5)
        # Create a style for the treeview heading with light cyan background
        style = ttk.Style()
        style.configure("Treeview.Heading", background="light cyan", font=("Arial", 10, "bold"), anchor="center")
        self.tree.bind("<Double-1>", self.view_edit_record)  # Double-click to open View/Edit window

        # Define column headings
        # Define column headings and set their properties
        for i, col in enumerate(columns):
            self.tree.heading(col, text=col)
            if i < 3:  # For the first 3 columns, set the anchor to "w" (west/left-aligned)
                self.tree.column(col, width=100, anchor="w")
            else:  # For the rest, keep the anchor as "center"
                self.tree.column(col, width=100, anchor="center")

        # Add scrollbars
        v_scroll = ttk.Scrollbar(self.data_display_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(self.data_display_frame, orient="horizontal", command=self.tree.xview)

        # Configure the Treeview to use the scrollbars
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Place tree and scrollbars

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both")

        # Load the last five entries initially
        self.load_last_entries()

        self.data_entry_window.focus()  # Focus on the new window
        self.data_entry_window.grab_set()  # Make the window modal

    def load_last_entries(self):
        """Loads the last 5 entries from the SQL database and displays them in the Treeview table."""
        # Database connection configuration
        db_config = serverdb_config

        try:
            # Establish connection
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Fetch last 5 entries from the database
            cursor.execute("""
                SELECT * FROM inward_logistic ORDER BY id DESC LIMIT 5
            """)
            last_five_entries = cursor.fetchall()

            print("entries", last_five_entries)

            # Clear existing data in the treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert last 5 entries into the treeview
            for entry in last_five_entries:
                self.tree.insert("", tk.END, values=list(entry))
                print(entry)

            for col in self.tree["columns"]:
                self.tree.column(col, anchor="center")  # Center-align column data

            # Update the Treeview
            self.tree.update_idletasks()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            # Close the database connection
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def save_data(self):
        """
        Saves the data entered in the form to an SQL database.
        """
        # Extract and convert all data to string
        data = [str(entry.get()) if isinstance(entry, (tk.Entry, tk.StringVar)) else
                entry.get_date().strftime('%m/%d/%y') if isinstance(entry, DateEntry) else
                str(entry.get('1.0', 'end-1c')) for entry in self.entry_fields]

        # Validate that the quantity (data[13]) is numeric
        if not re.match(r'^[0-9]+$', data[13]):
            messagebox.showerror("Error", "Qty must be numeric", parent=self.data_entry_window)
            return

        # Validate that the invoice number (data[6]) is not empty
        if data[6].strip() == "":
            messagebox.showerror("Error", "Invoice cannot be blank", parent=self.data_entry_window)
            return

        print("Date :", data[3], " ", data[4], "Return Date :", data[9], " ", data[10])

        # Convert Date and Time fields to correct format
        try:
            data[3] = datetime.strptime(data[3], '%m/%d/%y').strftime('%Y-%m-%d')  # Ensure date format is correct
            data[9] = datetime.strptime(data[9], '%m/%d/%y').strftime('%Y-%m-%d')  # Ensure return date is correct
            data[4] = data[4] if ":" in data[4] else "00:00:00"  # Ensure correct time format
            data[10] = data[10] if ":" in data[10] else "00:00:00"
            print("After formatting ---> Date :", data[3], " ", data[4], "Return Date :", data[9], " ", data[10])
        except ValueError as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Invalid Date or Time format", parent=self.data_entry_window)
            return

        # Database connection configuration
        try:
            # Establish connection
            conn = mysql.connector.connect(**serverdb_config)
            cursor = conn.cursor()

            # Define SQL query to insert data
            sql_query = """
                INSERT INTO inward_logistic (
                    Inward_No, Return_Type, Benefit_Type, Date, Time, Gate_Entry_No, Invoice_No, PO_No, BOE_No,
                    Return_Date, Return_Time, Supplier, Material, Qty, Department, Project, TPL_Name, Vehicle,
                    Received, Authorized, Security, Remark, TPL_Remarks
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Execute query
            cursor.execute(sql_query, data)
            conn.commit()

            # Notify the user that the data has been saved successfully
            messagebox.showinfo("Success", "Data saved successfully", parent=self.data_entry_window)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=self.data_entry_window)

        finally:
            # Close the database connection
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def reset_fields(self):
        """
        Clears the input fields in the data entry form.

        This method iterates over all the entry fields stored in the `self.entry_fields` list.
        If the field is a standard text entry (tk.Entry), it deletes any existing text,
        effectively resetting the input field to an empty state.

        This is useful for allowing users to reset the form quickly without manually clearing each field.
        """
        for entry in self.entry_fields:
            if isinstance(entry, tk.Entry):  # Check if the field is a standard text entry widget
                entry.delete(0, tk.END)  # Clear the text from the entry field

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
        self.view_edit_window = tk.Toplevel(self.data_entry_window)
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
            self.load_last_entries()

        edit_button = tk.Button(button_frame, text="Edit", command=enable_edit, bg="light cyan",font=('ariel narrow', 10), width=10)
        edit_button.pack(side="left", padx=5)
        self.save_button_edit = tk.Button(button_frame, text="Save", command=save_changes, bg="grey",font=('ariel narrow', 10), width=10,state=DISABLED)
        self.save_button_edit.pack(side="left", padx=5)
        close_button = tk.Button(button_frame, text="Close", command=self.view_edit_window.destroy, bg="light cyan",font=('ariel narrow', 10), width=10)
        close_button.pack(side="left", padx=5)

        self.view_edit_window.focus()




