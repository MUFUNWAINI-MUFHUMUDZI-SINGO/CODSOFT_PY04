import tkinter as tk
from tkinter import messagebox
import json

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        self.tasks = []

        # Load tasks from file if available
        self.load_tasks()

        # Task input fields
        tk.Label(root, text="1. Task Title:").pack()
        self.title_entry = tk.Entry(root, width=50)
        self.title_entry.pack()

        tk.Label(root, text="2. Task Description:").pack()
        self.desc_entry = tk.Text(root, height=5, width=50)
        self.desc_entry.pack()

        # Buttons with colors and commands
        tk.Button(root, text="Add Task", command=self.add_task, bg="lightblue").pack(pady=10)
        tk.Button(root, text="Mark Complete", command=self.mark_complete, bg="lightgreen").pack()
        tk.Button(root, text="Delete Task", command=self.delete_task, bg="lightcoral").pack()

        # Task list as a Listbox
        self.task_listbox = tk.Listbox(root, width=60, height=10)
        self.task_listbox.pack(pady=20)
        self.task_listbox.bind("<Double-Button-1>", self.on_task_select)  # Bind double-click event

        self.update_task_list()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get("1.0", tk.END)

        if title.strip() == "":
            messagebox.showwarning("Warning", "Task title cannot be empty!")
            return

        task = {"title": title, "description": description.strip(), "completed": False}
        self.tasks.append(task)
        self.update_task_list()
        self.save_tasks()

        # Clear input fields after adding task
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete("1.0", tk.END)

    def mark_complete(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.tasks[index]["completed"] = True
            self.update_task_list()
            self.save_tasks()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.tasks[index]
            self.update_task_list()
            self.save_tasks()

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.tasks, start=1):
            status = "✓" if task["completed"] else "◻"
            title = task['title']
            description = task['description']
            # Truncate description for display in listbox if too long
            if len(description) > 50:
                description = description[:50] + "..."
            self.task_listbox.insert(tk.END, f"{idx}. {status} {title}\n   {description}")

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=4)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []

    def on_task_select(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            # Handle task selection (can add more functionality here if needed)
            pass

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
