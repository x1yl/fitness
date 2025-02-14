# Fitness Tracker

A simple desktop application to track your workouts and calculate calories burned.

## Features

- Log different types of workouts (Running, Cycling, Swimming, etc.)
- Track duration and optional weights used
- Automatic calorie calculation based on:
  - Base calories per minute for each exercise type
  - Duration of workout
  - Additional calories when using weights
- View workout history in a table format
- See total workouts and calories burned
- Data persistence using JSON storage

## Installation

1. Make sure you have Python 3.x installed
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. To log a workout:
   - Select workout type from dropdown
   - Enter duration in minutes
   - Optionally enter weight used (in kg)
   - Click "Log Workout"

3. View your history:
   - Switch to "History" tab
   - See all workouts in chronological order
   - Check total workouts and calories at the top

## Data Storage

Workouts are stored in `fitness.json` in the same directory as the application.

## Supported Workouts

| Workout Type   | Calories per Minute |
|---------------|-------------------|
| Running       | 10               |
| Cycling       | 8                |
| Swimming      | 9                |
| Bench Press   | 6                |
| Squats        | 7                |
| Deadlift      | 8                |
| Yoga          | 4                |

## Calorie Calculation

- Base calories = (calories per minute) × (duration)
- If weight is used: Additional calories = (weight in kg × 0.5) × duration
- Total calories = Base calories + Additional calories