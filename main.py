import tkinter
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class FitnessTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Tracker")
        self.root.geometry("600x450")

        # workouts
        self.workouts = [
            {"name": "Running", "met": 10},
            {"name": "Cycling", "met": 8},
            {"name": "Swimming", "met": 9},
            {"name": "Bench Press", "met": 6},
            {"name": "Squats", "met": 7},
            {"name": "Deadlift", "met": 8},
            {"name": "Yoga", "met": 4},
        ]

        # intial setup
        self.history = self.load_history()
        self.setup_tabs()
        self.setup_workout_tab()
        self.setup_history_tab()

    def setup_tabs(self):
        # Create tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill="both", padx=5, pady=5)
        # Create frames for each tab
        self.workout_tab = ttk.Frame(self.tabs)
        self.history_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.workout_tab, text="Log Workout")
        self.tabs.add(self.history_tab, text="History")

    def setup_workout_tab(self):
        # all the stuff u see on the workout tab
        ttk.Label(
            self.workout_tab, text="Log Your Workout", font=("Arial", 14, "bold")
        ).pack(pady=10)
        # Workout selection
        ttk.Label(self.workout_tab, text="Select Workout:").pack(
            anchor="w", padx=10, pady=5
        )
        # Dropdown for workout selection
        self.workout_var = tkinter.StringVar()
        workout_names = [workout["name"] for workout in self.workouts]
        ttk.Combobox(
            self.workout_tab,
            textvariable=self.workout_var,
            values=workout_names,
            state="readonly",
        ).pack(fill="x", padx=10, pady=5)
        self.workout_var.set(workout_names[0])

        # Duration input
        ttk.Label(self.workout_tab, text="Duration (minutes):").pack(
            anchor="w", padx=10, pady=5
        )
        self.duration_var = tkinter.StringVar()
        ttk.Entry(self.workout_tab, textvariable=self.duration_var).pack(
            fill="x", padx=10, pady=5
        )

        # Weight input
        ttk.Label(self.workout_tab, text="Weight used (kg, optional):").pack(
            anchor="w", padx=10, pady=5
        )
        self.weight_var = tkinter.StringVar()
        ttk.Entry(self.workout_tab, textvariable=self.weight_var).pack(
            fill="x", padx=10, pady=5
        )

        # Log workout button
        ttk.Button(self.workout_tab, text="Log Workout", command=self.log_workout).pack(
            pady=20
        )

    def setup_history_tab(self):
        # all the stuff u see on the history tab
        ttk.Label(
            self.history_tab, text="Workout History", font=("Arial", 14, "bold")
        ).pack(pady=10)
        self.summary_label = ttk.Label(self.history_tab, text="")
        self.summary_label.pack(pady=5)

        # Table setup
        cols = ("Date", "Workout", "Duration", "Weight", "Calories")
        self.table = ttk.Treeview(self.history_tab, columns=cols, show="headings")
        for col in cols:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)
        self.table.pack(expand=True, fill="both", padx=10, pady=10)

        self.refresh_history()

    # Load history from JSON file
    def load_history(self):
        if not os.path.exists('fitness.json'):
            with open('fitness.json', 'w') as f:
                json.dump([], f)
        try:
            with open("fitness.json", "r") as f:
                return json.load(f)
        except:
            return []

    def save_workout(self, workout):
        # Save workout to JSON file
        self.history.append(workout)
        with open("fitness.json", "w") as f:
            json.dump(self.history, f)

    def calculate_calories(self, base_met, duration, weight=None):
        # Calculate calories burned based on met and duration
        calories = base_met * 3.5 * (duration/200)
        if weight:
            calories = base_met * (weight * 0.25 ) * 3.5 * (duration/200)
        return round(calories)

    def log_workout(self):
        try:
            # Get inputs
            workout_name = self.workout_var.get()
            duration = int(self.duration_var.get())
            weight_str = self.weight_var.get()
            weight = float(weight_str) if weight_str else None

            # Validate inputs
            if duration <= 0:
                messagebox.showerror("Error", "Duration must be positive")
                return
            if weight is not None and weight <= 0:
                messagebox.showerror("Error", "Weight must be positive if provided")
                return

            # Find workout and calculate calories
            selected_workout = None
            for workout in self.workouts:
                if workout["name"] == workout_name:
                    selected_workout = workout
                    break
            calories = self.calculate_calories(
                selected_workout["met"], duration, weight
            )

            # Save workout
            new_workout = {
                "name": workout_name,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "duration": duration,
                "weight": weight,
                "calories": calories,
            }
            self.save_workout(new_workout)
            self.refresh_history()

            # Clear input fields
            self.duration_var.set("")
            self.weight_var.set("")
            messagebox.showinfo(
                "Success", f"Workout logged! Calories burned: {calories}"
            )

        except ValueError:
            messagebox.showerror("Error", "Invalid input values")

    def refresh_history(self):
        # Clear existing entries
        for row in self.table.get_children():
            self.table.delete(row)

        # Add workouts (newest first)
        total_calories = 0
        for workout in reversed(self.history):
            # display weight if provided, else "N/A"
            weight_display = (
                f"{workout['weight']} kg" if workout.get("weight") else "N/A"
            )
            # Add into table
            self.table.insert(
                "",
                "end",
                values=(
                    workout["date"],
                    workout["name"],
                    f"{workout['duration']} min",
                    weight_display,
                    workout["calories"],
                ),
            )
            # Calculate total calories
            total_calories += workout["calories"]

        # Update total calories and workout count
        self.summary_label.config(
            text=f"Total workouts: {len(self.history)} | Total calories burned: {total_calories}"
        )


# main
if __name__ == "__main__":
    root = tkinter.Tk()
    app = FitnessTracker(root)
    root.mainloop()
