import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Setup
conn = sqlite3.connect("hotel_staff.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    phone TEXT,
    salary TEXT
)
""")
conn.commit()

# Main App
class StaffManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("HMS PRO - Staff Management")
        self.root.geometry("900x500")
        self.root.configure(bg="#f4f6f9")

        title = tk.Label(root, text="STAFF MANAGEMENT",
                         font=("Arial", 20, "bold"),
                         bg="#f4f6f9", fg="#2c3e50")
        title.pack(pady=10)

        # Form Frame
        form_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        form_frame.place(x=20, y=70, width=350, height=400)

        tk.Label(form_frame, text="Name", font=("Arial", 12), bg="white").pack(pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        tk.Label(form_frame, text="Role", font=("Arial", 12), bg="white").pack(pady=5)
        self.role_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.role_entry.pack(pady=5)

        tk.Label(form_frame, text="Phone", font=("Arial", 12), bg="white").pack(pady=5)
        self.phone_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.phone_entry.pack(pady=5)

        tk.Label(form_frame, text="Salary", font=("Arial", 12), bg="white").pack(pady=5)
        self.salary_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.salary_entry.pack(pady=5)

        # Buttons
        tk.Button(form_frame, text="Add Staff", bg="#27ae60", fg="white",
                  font=("Arial", 12), command=self.add_staff).pack(pady=10)

        tk.Button(form_frame, text="Update Staff", bg="#2980b9", fg="white",
                  font=("Arial", 12), command=self.update_staff).pack(pady=5)

        tk.Button(form_frame, text="Delete Staff", bg="#c0392b", fg="white",
                  font=("Arial", 12), command=self.delete_staff).pack(pady=5)

        tk.Button(form_frame, text="Clear", bg="#7f8c8d", fg="white",
                  font=("Arial", 12), command=self.clear_fields).pack(pady=5)

        # Table Frame
        table_frame = tk.Frame(root, bd=2, relief=tk.RIDGE)
        table_frame.place(x=400, y=70, width=480, height=400)

        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

        self.staff_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Role", "Phone", "Salary"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.staff_table.xview)
        scroll_y.config(command=self.staff_table.yview)

        self.staff_table.heading("ID", text="ID")
        self.staff_table.heading("Name", text="Name")
        self.staff_table.heading("Role", text="Role")
        self.staff_table.heading("Phone", text="Phone")
        self.staff_table.heading("Salary", text="Salary")
        self.staff_table["show"] = "headings"

        self.staff_table.pack(fill=tk.BOTH, expand=1)
        self.staff_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.show_staff()

    # Add Staff
    def add_staff(self):
        if self.name_entry.get() == "":
            messagebox.showerror("Error", "Name is required")
            return

        cursor.execute("INSERT INTO staff (name, role, phone, salary) VALUES (?, ?, ?, ?)",
                       (self.name_entry.get(),
                        self.role_entry.get(),
                        self.phone_entry.get(),
                        self.salary_entry.get()))
        conn.commit()
        self.show_staff()
        self.clear_fields()
        messagebox.showinfo("Success", "Staff Added Successfully")

    # Show Staff
    def show_staff(self):
        cursor.execute("SELECT * FROM staff")
        rows = cursor.fetchall()
        self.staff_table.delete(*self.staff_table.get_children())
        for row in rows:
            self.staff_table.insert("", tk.END, values=row)

    # Get Selected Row
    def get_cursor(self, event=""):
        row = self.staff_table.focus()
        content = self.staff_table.item(row)
        data = content["values"]

        if data:
            self.clear_fields()
            self.name_entry.insert(0, data[1])
            self.role_entry.insert(0, data[2])
            self.phone_entry.insert(0, data[3])
            self.salary_entry.insert(0, data[4])
            self.selected_id = data[0]

    # Update Staff
    def update_staff(self):
        try:
            cursor.execute("""UPDATE staff SET name=?, role=?, phone=?, salary=? WHERE id=?""",
                           (self.name_entry.get(),
                            self.role_entry.get(),
                            self.phone_entry.get(),
                            self.salary_entry.get(),
                            self.selected_id))
            conn.commit()
            self.show_staff()
            self.clear_fields()
            messagebox.showinfo("Success", "Staff Updated Successfully")
        except:
            messagebox.showerror("Error", "Select a staff record first")

    # Delete Staff
    def delete_staff(self):
        try:
            cursor.execute("DELETE FROM staff WHERE id=?", (self.selected_id,))
            conn.commit()
            self.show_staff()
            self.clear_fields()
            messagebox.showinfo("Success", "Staff Deleted Successfully")
        except:
            messagebox.showerror("Error", "Select a staff record first")

    # Clear Fields
    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = StaffManagement(root)
    root.mainloop()
