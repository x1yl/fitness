# give a idea of how to make a python fitness tracker with pygui
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import json
import datetime

class FitnessTracker:
    def __init__(self, master):
        self.master = master
        self.master.title('Fitness Tracker')
        self.master.geometry('600x600')
        self.master.resizable(True, True)
        self.master.config(bg='lightblue')

        self.workout = tk.StringVar()
        self.workout.set('')

        self.workout_label = tk.Label(self.master, text='Workout:', bg='lightblue')
        self.workout_label.pack()

        self.workout_entry = tk.Entry(self.master, textvariable=self.workout)
        self.workout_entry.pack()

        self.save_button = tk.Button(self.master, text='Save', command=self.save_workout)
        self.save_button.pack()

        self.load_button = tk.Button(self.master, text='Load', command=self.load_workout)
        self.load_button.pack()

        self.quit_button = tk.Button(self.master, text='Quit', command=self.quit)
        self.quit_button.pack()

    def save_workout(self):
        workout = self.workout.get()
        if workout == '':
            messagebox.showerror('Error', 'Workout cannot be empty!')
            return
        filename = 'fitness.json'
        if messagebox.askyesno('Save', 'Are you sure you want to save the workout?'):
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data.append({'workout': workout, 'date': date})
            with open(filename, 'w') as f:
                json.dump(data, f)
            messagebox.showinfo('Success', f'Workout saved successfully!\nWorkout: {workout}\nDate: {date}')
            self.workout.set('')
    def load_workout(self):
        filename = 'fitness.json'
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror('Error', 'No workouts found!')
            return
        workouts = ''
        for workout in data:
            workouts += f"Workout: {workout['workout']}\nDate: {workout['date']}\n\n"
        messagebox.showinfo('Workouts', workouts)

    def quit(self):
        if messagebox.askyesno('Quit', 'Are you sure you want to quit?'):
            self.master.destroy()
            
if __name__ == '__main__':
    root = tk.Tk()
    app = FitnessTracker(root)
    root.mainloop()
