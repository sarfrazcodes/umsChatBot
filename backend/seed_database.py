import os
import pandas as pd
from app import create_app
from extensions import db
import models

def seed():
    app = create_app()
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        mock_dir = os.path.join(os.path.dirname(__file__), 'mock_data')
        
        # Define the exact order to respect foreign key constraints
        seed_order = [
            ('users.csv', models.User),
            ('students.csv', models.Student),
            ('subjects.csv', models.Subject),
            ('faculty.csv', models.Faculty),
            ('faculty_leave.csv', models.FacultyLeave),
            ('timetable.csv', models.Timetable),
            ('attendance.csv', models.Attendance),
            ('exams.csv', models.Exam),
            ('fees.csv', models.Fee),
            ('messages.csv', models.Message),
            ('placement_drives.csv', models.PlacementDrive),
            ('placement_registrations.csv', models.PlacementRegistration),
            ('leaves.csv', models.Leave),
            ('rms_categories.csv', models.RMSCategory),
            ('rms_requests.csv', models.RMSRequest),
            ('library_books.csv', models.LibraryBook),
            ('grading_rules.csv', models.GradingRules),
            ('student_marks.csv', models.StudentMarks)
        ]
        
        for filename, model in seed_order:
            filepath = os.path.join(mock_dir, filename)
            if os.path.exists(filepath):
                try:
                    df = pd.read_csv(filepath)
                    if not df.empty:
                        from datetime import datetime, date, time
                        # Convert DataFrame to list of dictionaries
                        records = df.to_dict(orient='records')
                        
                        # Handle NaNs and Dates
                        for record in records:
                            for k, v in record.items():
                                if pd.isna(v):
                                    record[k] = None
                                elif isinstance(v, str):
                                    # Simple heuristic to convert date/time strings
                                    if len(v) == 10 and v.count('-') == 2:
                                        try:
                                            record[k] = datetime.strptime(v, '%Y-%m-%d').date()
                                        except: pass
                                    elif len(v) == 8 and v.count(':') == 2:
                                        try:
                                            record[k] = datetime.strptime(v, '%H:%M:%S').time()
                                        except: pass
                                    elif len(v) == 19 and v.count('-') == 2 and v.count(':') == 2:
                                        try:
                                            record[k] = datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
                                        except: pass
                                    
                        db.session.bulk_insert_mappings(model, records)
                        db.session.commit()
                        print(f"Successfully seeded {filename} ({len(records)} rows)")
                    else:
                        print(f"Skipped {filename} (Empty)")
                except Exception as e:
                    db.session.rollback()
                    print(f"Error seeding {filename}: {e}")
            else:
                print(f"File not found: {filename}")
                
        print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
