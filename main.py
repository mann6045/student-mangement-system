import tkinter as tk
from app_ui import StudentApp

if __name__ == "__main__":
    # Ensure the database and table are ready before starting the app
    import database as db
    db.connect_db()

    # Create and run the application
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
