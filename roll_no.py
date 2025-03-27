import pandas as pd
from datetime import datetime

path = 'C:/Users/Admin/Downloads/Data Engineering/Data Engineering/data - sample.xlsx'
df = pd.read_excel(path)

df['attendance_date'] = pd.to_datetime(df['attendance_date'])

df = df.sort_values(by=['student_id', 'attendance_date'])

def extract_absence_streaks(data):
  
    absence_streaks = []
    
    prev_student = None
    streak_start = None
    streak_length = 0

    for index, record in data.iterrows():
        student = record['student_id']
        date = record['attendance_date']
        status = record['status']
        
        if student != prev_student:
            if prev_student is not None and streak_length > 3:
                absence_streaks.append({
                    'student_id': prev_student,
                    'absence_start': streak_start,
                    'absence_end': prev_date,
                    'absent_days': streak_length
                })

            prev_student = student
            streak_start = None
            streak_length = 0
        
        if status == 'Absent':
            if streak_length == 0:
                streak_start = date
            streak_length += 1
        else:
            if streak_length > 3:
                absence_streaks.append({
                    'student_id': prev_student,
                    'absence_start': streak_start,
                    'absence_end': prev_date,
                    'absent_days': streak_length
                })
            streak_length = 0
        
        prev_date = date
    
    if streak_length > 3:
        absence_streaks.append({
            'student_id': prev_student,
            'absence_start': streak_start,
            'absence_end': prev_date,
            'absent_days': streak_length
        })

    return absence_streaks

streaks = extract_absence_streaks(df)

absence_df = pd.DataFrame(streaks)

if not absence_df.empty:
    print(absence_df)
else:
    print("No student had more than 3 consecutive absence days.")
