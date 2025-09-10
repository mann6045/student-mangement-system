# student-mangement-system
• Designed and developed a Student Management System using Python, implementing CRUD operations for efficient data handling. • Optimized data storage and retrieval by integrating a SQLite database, ensuring data consistency and reducing errors.

### **Key Improvements in This Version**

1.  **Professional UI/UX:** The layout is split into logical sections (form on the left, records on the right). It uses padding and modern-looking `ttk` widgets for a clean, user-friendly experience.
    
2.  **Separation of Concerns:** The UI (`app_ui.py`), database logic (`database.py`), and application entry point (`main.py`) are all in separate files, making the project much easier to maintain and expand.
3.  **Detailed Information:** The form now captures all the additional details you requested.
4.  **Robust Input Validation:**
    * Checks for empty required fields.
    * Ensures the mobile number is exactly 10 digits.
    * Validates the email format using a regular expression.
    * Checks for a valid age.
    * The "Gender" field is a dropdown (`Combobox`) to prevent invalid entries.
5.  **User-Friendly Feedback:** A status bar at the bottom provides clear, non-intrusive feedback for actions like adding, updating, or deleting students. Error messages are shown in clear pop-up windows.

### **How to Run the Project**

The process remains the same:

1.  Make sure all four files (`main.py`, `app_ui.py`, `database.py`, `student.py`) are in the same folder.
2.  Open your terminal and navigate to that folder.
3.  Run the main script:
    ```bash
    python main.py
