import pandas as pd
from datetime import datetime

file_path = 'C:/Users/Admin/Downloads/Data Engineering/Data Engineering/data - sample.xlsx'
df = pd.read_excel(file_path)

df['attendance_date'] = pd.to_datetime(df['attendance_date'])

df = df.sort_values(by=['student_id', 'attendance_date'])

def find_absence_streaks(df):

    latest_absence_streak = []

    current_student = None
    streak_start_date = None
    streak_count = 0

    for index, row in df.iterrows():
        student_id = row['student_id']
        date = row['attendance_date']
        status = row['status']

        if student_id != current_student:
            if current_student is not None and streak_count > 3:
                latest_absence_streak.append({
                    'student_id': current_student,
                    'absence_start_date': streak_start_date,
                    'absence_end_date': previous_date,
                    'total_absent_days': streak_count
                })

            current_student = student_id
            streak_start_date = None
            streak_count = 0

        if status == 'Absent':
            if streak_count == 0:  
                streak_start_date = date
            streak_count += 1
        else:
            if streak_count > 3:  
                latest_absence_streak.append({
                    'student_id': current_student,
                    'absence_start_date': streak_start_date,
                    'absence_end_date': previous_date,
                    'total_absent_days': streak_count
                })
            streak_count = 0

        previous_date = date
    
    if streak_count > 3:
        latest_absence_streak.append({
            'student_id': current_student,
            'absence_start_date': streak_start_date,
            'absence_end_date': previous_date,
            'total_absent_days': streak_count
        })

    return latest_absence_streak

absence_streaks = find_absence_streaks(df)

absence_df = pd.DataFrame(absence_streaks)

if not absence_df.empty:
    print(absence_df)
else:
    print("No absence streaks longer than 3 days found.")
