from common_utils import *

class SettingsWindow:
    def __init__(self, parent):
        self.modify_window = None
        self.parent = parent
        self.settings_window = tk.Toplevel()
        self.width, self.height = pyautogui.size()
        self.settings_window.title("Settings")
        self.settings_window.geometry('{}x{}+{}+{}'.format(450, 250, int(self.width / 3), int(self.height / 3.2)))
        self.settings_window.configure(bg='wheat')

        # Create the menu bar
        self.menu_bar = tk.Menu(self.settings_window)
        self.settings_window.config(menu=self.menu_bar)

        # Create the 'Projects' menu
        self.projects_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Projects", menu=self.projects_menu)
        self.projects_menu.add_command(label="Create", command=self.create_project)
        self.projects_menu.add_command(label="Modify", command=self.modify_project)

        # Create the 'Users' menu
        self.users_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Users", menu=self.users_menu)
        self.users_menu.add_command(label="Create", command=self.create_user)
        self.users_menu.add_command(label="Change Password", command=self.change_password)

        self.settings_window.mainloop()

    def create_project(self):
        self.project_window = tk.Toplevel(self.settings_window)
        self.project_window.title("Create Project")
        self.project_window.geometry('{}x{}+{}+{}'.format(480, 120, int(self.width / 2.6), int(self.height / 3)))
        self.project_window.configure(bg='wheat')

        lbl_add_project = tk.Label(self.project_window, text="New Project Name:", font=('ariel narrow', 12), bg='wheat')
        lbl_add_project.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_project_name = tk.Entry(self.project_window, width=35, font=('ariel narrow', 10), bg='light yellow')
        self.entry_project_name.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Create a frame for the buttons
        button_frame = tk.Frame(self.project_window, width=200, height=100, bd=4, relief='ridge', bg='wheat')
        button_frame.grid(row=1, column=0, columnspan=2, pady=20)

        # Add buttons to the button frame
        btn_save_project = tk.Button(button_frame, text="Save", command=self.save_project,
                                     font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_save_project.grid(row=0, column=0, padx=5, pady=5)

        btn_close_project = tk.Button(button_frame, text="Close", command=self.project_window.destroy,
                                      font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_close_project.grid(row=0, column=1, padx=5, pady=5)

        # Center the button frame in the window
        #self.project_window.grid_rowconfigure(1, weight=1)
        self.project_window.grid_columnconfigure(0, weight=1)
        self.project_window.grid_columnconfigure(1, weight=1)

    def modify_project(self):
        self.modify_window = tk.Toplevel(self.settings_window)
        self.modify_window.title("Modify Project")
        self.modify_window.geometry('{}x{}+{}+{}'.format(480, 135, int(self.width / 2.6), int(self.height / 3)))
        self.modify_window.configure(bg='wheat')

        lbl_modify_project = tk.Label(self.modify_window, text="Modify Project:", font=('ariel narrow', 12), bg='wheat')
        lbl_modify_project.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.project_dropdown = ttk.Combobox(self.modify_window, font=('ariel narrow', 10), state="readonly", width=38)
        self.project_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        lbl_new_project = tk.Label(self.modify_window, text="New Name:", font=('ariel narrow', 12), bg='wheat')
        lbl_new_project.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry_modify_project = tk.Entry(self.modify_window, width=40, font=('ariel narrow', 10), bg='light yellow')
        self.entry_modify_project.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Create a frame for the buttons
        button_frame = tk.Frame(self.modify_window, width=200, height=100, bd=4, relief='ridge', bg='wheat')
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        # Add buttons to the button frame
        btn_modify_project = tk.Button(button_frame, text="Save", command=self.update_project,
                                     font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_modify_project.grid(row=0, column=0, padx=5, pady=5)

        btn_close_project = tk.Button(button_frame, text="Close", command=self.modify_window.destroy,
                                      font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_close_project.grid(row=0, column=1, padx=5, pady=5)

        # Center the button frame in the window
        # self.modify_window.grid_rowconfigure(1, weight=1)
        self.modify_window.grid_columnconfigure(0, weight=1)
        self.modify_window.grid_columnconfigure(1, weight=1)


    def create_user(self):
        self.user_window = tk.Toplevel(self.settings_window)
        self.user_window.title("Create User")
        self.user_window.geometry('{}x{}+{}+{}'.format(400, 250, int(self.width / 2.6), int(self.height / 3)))
        self.user_window.configure(bg='wheat')

        lbl_username = tk.Label(self.user_window, text="Username:", font=('ariel narrow', 12), bg='wheat')
        lbl_username.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_username = tk.Entry(self.user_window, width=40, font=('ariel narrow', 10), bg='light yellow')
        self.entry_username.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        lbl_password = tk.Label(self.user_window, text="Password:", font=('ariel narrow', 12), bg='wheat')
        lbl_password.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry_password = tk.Entry(self.user_window, width=40, font=('ariel narrow', 10), show="*",
                                       bg='light yellow')
        self.entry_password.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        lbl_category = tk.Label(self.user_window, text="Category:", font=('ariel narrow', 12), bg='wheat')
        lbl_category.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.category_var = tk.StringVar()
        self.category_var.set("User")
        category_dropdown = ttk.Combobox(self.user_window, textvariable=self.category_var, state="readonly",
                                         values=["User", "Admin"], font=('ariel narrow', 10), width=38)
        category_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        btn_save_user = tk.Button(self.user_window, text="Save User", command=self.save_user,
                                  font=('ariel narrow', 10), width=10, bg='light cyan')
        btn_save_user.grid(row=3, column=0, padx=5, pady=5)

    def change_password(self):
        self.password_window = tk.Toplevel(self.settings_window)
        self.password_window.title("Change Password")
        self.password_window.geometry('{}x{}+{}+{}'.format(400, 200, int(self.width / 2.6), int(self.height / 3)))
        self.password_window.configure(bg='wheat')

        lbl_username = tk.Label(self.password_window, text="Username:", font=('ariel narrow', 12), bg='wheat')
        lbl_username.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_username = tk.Entry(self.password_window, width=40, font=('ariel narrow', 10), bg='light yellow')
        self.entry_username.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        lbl_new_password = tk.Label(self.password_window, text="New Password:", font=('ariel narrow', 12), bg='wheat')
        lbl_new_password.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry_new_password = tk.Entry(self.password_window, width=40, font=('ariel narrow', 10), show="*",
                                           bg='light yellow')
        self.entry_new_password.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        btn_change_password = tk.Button(self.password_window, text="Change Password", command=self.update_password,
                                        font=('ariel narrow', 10), width=15, bg='light cyan')
        btn_change_password.grid(row=2, column=0, padx=5, pady=5)

    def save_project(self):
        project_name = self.entry_project_name.get().strip()
        if project_name:
            db_config = serverdb_config
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("USE logistic")
                query = "SELECT * FROM projects WHERE project_name = %s"
                cursor.execute(query, (project_name,))
                if cursor.fetchone():
                    messagebox.showwarning("Warning", "Project already exists!")
                else:
                    query = "INSERT INTO projects (project_name, tpl_name) VALUES (%s, %s)"
                    cursor.execute(query, (project_name, None))
                    conn.commit()
                    messagebox.showinfo("Success", "Project Added Successfully")
                    self.entry_project_name.delete(0, tk.END)
                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                root = tk.Tk()
                root.withdraw()
                response = messagebox.askokcancel("Connection Error", "Could not connect to server. Application will close.")
                if response:
                    root.destroy()
                    sys.exit(1)
                print(f"Error: {err}")
        else:
            messagebox.showwarning("Warning", "Enter a valid project name!")

    def update_project(self):
        selected_project = self.project_dropdown.get().strip()
        new_project_name = self.entry_modify_project.get().strip()
        if not selected_project:
            messagebox.showwarning("Warning", "No project selected!")
            return
        if not new_project_name:
            messagebox.showwarning("Warning", "Enter a new project name!")
            return
        db_config = serverdb_config
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("USE logistic")
            query = "SELECT * FROM projects WHERE project_name = %s"
            cursor.execute(query, (selected_project,))
            if cursor.fetchone():
                query = "UPDATE projects SET project_name = %s WHERE project_name = %s"
                cursor.execute(query, (new_project_name, selected_project))
                conn.commit()
                messagebox.showinfo("Success", "Project Modified Successfully")
                self.entry_modify_project.delete(0, tk.END)
            else:
                messagebox.showwarning("Warning", "Selected project not found!")
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            root = tk.Tk()
            root.withdraw()
            response = messagebox.askokcancel("Connection Error", "Could not connect to server. Application will close.")
            if response:
                root.destroy()
                sys.exit(1)
            print(f"Error: {err}")


    def save_user(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        category = self.category_var.get().strip()
        if username and password and category:
            db_config = serverdb_config
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("USE logistic")
                query = "SELECT * FROM login_users WHERE user_name = %s"
                cursor.execute(query, (username,))
                if cursor.fetchone():
                    messagebox.showwarning("Warning", "User already exists!")
                else:
                    query = "INSERT INTO login_users (user_name, password, category) VALUES (%s, %s, %s)"
                    cursor.execute(query, (username, password, category))
                    conn.commit()
                    messagebox.showinfo("Success", "User Created Successfully")
                    self.entry_username.delete(0, tk.END)
                    self.entry_password.delete(0, tk.END)
                    self.category_var.set("User")
                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                root = tk.Tk()
                root.withdraw()
                response = messagebox.askokcancel("Connection Error",
                                                  "Could not connect to server. Application will close.")
                if response:
                    root.destroy()
                    sys.exit(1)
                print(f"Error: {err}")
        else:
            messagebox.showwarning("Warning", "Enter valid user details!")


    def update_password(self):
        username = self.entry_username.get().strip()
        new_password = self.entry_new_password.get().strip()
        if username and new_password:
            db_config = serverdb_config
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("USE logistic")
                query = "SELECT * FROM login_users WHERE user_name = %s"
                cursor.execute(query, (username,))
                if cursor.fetchone():
                    query = "UPDATE login_users SET password = %s WHERE user_name = %s"
                    cursor.execute(query, (new_password, username))
                    conn.commit()
                    messagebox.showinfo("Success", "Password Changed Successfully")
                    self.entry_new_password.delete(0, tk.END)
                else:
                    messagebox.showwarning("Warning", "User not found!")
                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                root = tk.Tk()
                root.withdraw()
                response = messagebox.askokcancel("Connection Error",
                                                  "Could not connect to server. Application will close.")
                if response:
                    root.destroy()
                    sys.exit(1)
                print(f"Error: {err}")
        else:
            messagebox.showwarning("Warning", "Enter valid username and new password!")


    def load_projects(self):
        if os.path.exists("projects.txt"):
            with open("projects.txt", "r") as file:
                projects = file.read().splitlines()
                self.project_dropdown["values"] = projects
                if projects:
                    self.project_dropdown.set(projects[0])
                else:
                    self.project_dropdown["values"] = []
                    self.project_dropdown.set("")
        else:
            self.project_dropdown["values"] = []
            self.project_dropdown.set("")