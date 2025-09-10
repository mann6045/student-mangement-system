import tkinter as tk
from tkinter import ttk, messagebox
import re
import database as db

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Student Management System")
        self.root.geometry("1250x700")
        self.root.configure(bg="#f0f0f0")

        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("Helvetica", 11), background="#f0f0f0")
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=5)
        style.configure("TEntry", font=("Helvetica", 11), padding=5)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.configure("TCombobox", font=("Helvetica", 11), padding=5)
        style.configure("TLabelframe", labelanchor="n", background="#f0f0f0")
        style.configure("TLabelframe.Label", font=("Helvetica", 12, "bold"), background="#f0f0f0")

        # --- Main Frames ---
        form_frame = ttk.LabelFrame(root, text="Student Information", padding=(20, 10))
        form_frame.pack(side="left", fill="y", padx=10, pady=10)

        records_frame = ttk.Frame(root)
        records_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # --- Search/Filter Frame ---
        search_frame = ttk.LabelFrame(records_frame, text="Search Records", padding=(10, 5))
        search_frame.pack(fill="x", padx=10, pady=5)
        
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        ttk.Button(search_frame, text="Search", command=self.search_student).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Show All", command=self.populate_list).pack(side="left", padx=5)

        # --- Treeview for Displaying Students ---
        tree_container = ttk.Frame(records_frame)
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- UPDATED: Added "Class" to the columns ---
        columns = ("id", "name", "father_name", "mobile", "class", "school_name")
        self.tree = ttk.Treeview(tree_container, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("father_name", text="Father's Name")
        self.tree.heading("mobile", text="Mobile No.")
        self.tree.heading("class", text="Class") # New heading
        self.tree.heading("school_name", text="School Name")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("name", width=150)
        self.tree.column("father_name", width=150)
        self.tree.column("mobile", width=110)
        self.tree.column("class", width=80, anchor=tk.CENTER) # New column
        self.tree.column("school_name", width=180)
        
        self.tree.tag_configure('selected', background='#a6d8f5')

        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

        # --- Form Widgets ---
        self.create_form_widgets(form_frame)

        # --- Status Bar ---
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#dfdfdf")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.populate_list()

    def create_form_widgets(self, parent_frame):
        fields = {
            "Full Name:": "name_entry", "Father's Name:": "father_name_entry", "Age:": "age_entry",
            "Gender:": "gender_combobox", "School Name:": "school_entry", "Class:": "class_entry",
            "Division:": "division_entry", "Mobile Number:": "mobile_entry", "Email ID:": "email_entry",
            "Address:": "address_text"
        }
        
        row_num = 0
        for label_text, widget_name in fields.items():
            label = ttk.Label(parent_frame, text=label_text)
            label.grid(row=row_num, column=0, sticky="w", padx=5, pady=8)
            
            if widget_name == "gender_combobox":
                self.gender_combobox = ttk.Combobox(parent_frame, values=["Male", "Female", "Other"], width=28, state="readonly")
                self.gender_combobox.grid(row=row_num, column=1, sticky="ew", padx=5, pady=8)
            elif widget_name == "address_text":
                self.address_text = tk.Text(parent_frame, height=4, width=30, font=("Helvetica", 11))
                self.address_text.grid(row=row_num, column=1, sticky="ew", padx=5, pady=8)
            else:
                entry = ttk.Entry(parent_frame, width=30)
                entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=8)
                setattr(self, widget_name, entry)
            row_num += 1

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=row_num, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add", command=self.add_student).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_student).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_student).grid(row=0, column=2, padx=5)
        # --- FIX: Point 'Clear' button to the correct new function ---
        ttk.Button(button_frame, text="Clear", command=self.clear_form_and_selection).grid(row=0, column=3, padx=5)

    def get_form_data(self):
        return {
            "name": self.name_entry.get(), "father_name": self.father_name_entry.get(), "age": self.age_entry.get(),
            "gender": self.gender_combobox.get(), "school_name": self.school_entry.get(), "class": self.class_entry.get(),
            "division": self.division_entry.get(), "mobile_number": self.mobile_entry.get(),
            "email_id": self.email_entry.get(), "address": self.address_text.get("1.0", tk.END).strip()
        }

    def validate_inputs(self, data):
        required_fields = ["name", "father_name", "age", "gender", "mobile_number", "email_id"]
        if not all(data[field] for field in required_fields):
            messagebox.showerror("Validation Error", "Please fill all required fields: Name, Father's Name, Age, Gender, Mobile, and Email.")
            return False
        
        if not data["age"].isdigit() or not (0 < int(data["age"]) < 100):
            messagebox.showerror("Validation Error", "Please enter a valid age (e.g., 1 to 99).")
            return False

        if not re.match(r'^\d{10}$', data["mobile_number"]):
            messagebox.showerror("Validation Error", "Mobile number must be exactly 10 digits.")
            return False

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data["email_id"]):
            messagebox.showerror("Validation Error", "Please enter a valid email address.")
            return False
        return True

    def execute_db_action(self, action, success_msg, *args):
        try:
            action(*args)
            self.status_bar.config(text=success_msg)
            self.populate_list()
            self.clear_form_and_selection()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def add_student(self):
        data = self.get_form_data()
        if not self.validate_inputs(data):
            return
        data['age'] = int(data['age'])
        self.execute_db_action(db.add_student, f"Success: Student '{data['name']}' added.", data)

    def update_student(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select a student to update.")
            return
            
        student_id = int(self.tree.item(selected_items[0])['values'][0])
        data = self.get_form_data()
        if not self.validate_inputs(data):
            return
        data['age'] = int(data['age'])
        self.execute_db_action(db.update_student, f"Success: Student ID {student_id} updated.", student_id, data)

    def delete_student(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select a student to delete.")
            return

        student_id = int(self.tree.item(selected_items[0])['values'][0])
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID {student_id}? This action cannot be undone."):
            self.execute_db_action(db.delete_student, f"Success: Student ID {student_id} has been deleted.", student_id)

    def search_student(self):
        query = self.search_entry.get()
        if not query:
            self.populate_list()
            return
        results = db.search_students(query)
        self.update_treeview(results)
        self.status_bar.config(text=f"Showing {len(results)} results for '{query}'")

    def update_treeview(self, records):
        self.tree.delete(*self.tree.get_children())
        for row in records:
            # --- UPDATED: Add class (row[5]) to the values tuple ---
            self.tree.insert("", "end", values=(row[0], row[1], row[9], row[7], row[5], row[4]))

    def populate_list(self):
        all_students = db.get_all_students()
        self.update_treeview(all_students)
        self.status_bar.config(text=f"Ready. Total records: {len(all_students)}")
        self.search_entry.delete(0, tk.END)

    def on_item_select(self, event):
        for item in self.tree.get_children():
            self.tree.item(item, tags=())

        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        selected_item = selected_items[0]
        self.tree.item(selected_item, tags=('selected',))

        # --- This now calls the safe version of clear_fields ---
        self.clear_fields()

        student_id = int(self.tree.item(selected_item)['values'][0])
        
        all_students = db.get_all_students()
        student_data = next((s for s in all_students if s[0] == student_id), None)
        
        if student_data:
            (id, name, age, gender, school, s_class, division, mobile, email, father, address) = student_data
            self.name_entry.insert(0, name)
            self.father_name_entry.insert(0, father)
            self.age_entry.insert(0, str(age))
            self.gender_combobox.set(gender)
            self.school_entry.insert(0, school)
            self.class_entry.insert(0, s_class)
            self.division_entry.insert(0, division)
            self.mobile_entry.insert(0, mobile)
            self.email_entry.insert(0, email)
            self.address_text.insert("1.0", address)
            self.status_bar.config(text=f"Viewing details for Student ID: {id}")

    # --- FIX: This function now ONLY clears the form fields ---
    def clear_fields(self):
        """A helper function that ONLY clears the form entry widgets."""
        self.name_entry.delete(0, tk.END)
        self.father_name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_combobox.set('')
        self.school_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.division_entry.delete(0, tk.END)
        self.mobile_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_text.delete("1.0", tk.END)
        
    # --- NEW: A dedicated function for the 'Clear' button ---
    def clear_form_and_selection(self):
        """Command for the 'Clear' button. Clears the form and deselects from the tree."""
        self.clear_fields()
        if self.tree.selection():
            selected_item = self.tree.selection()[0]
            self.tree.item(selected_item, tags=()) # Remove highlight
            self.tree.selection_remove(selected_item)
        self.status_bar.config(text="Ready")
        self.name_entry.focus()

