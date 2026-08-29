import os
import csv
import random
from datetime import datetime, timedelta

MOCK_DIR = os.path.join(os.path.dirname(__file__), "mock_data")
os.makedirs(MOCK_DIR, exist_ok=True)

def generate_books():
    categories = ['Programming', 'Data Structures', 'Algorithms', 'Database', 'AI/ML', 'Cybersecurity', 'Web Development', 'Finance', 'Stocks/Investing', 'Mathematics', 'Physics', 'Business', 'Entrepreneurship', 'General Reading']
    
    books = []
    # Explicitly requested books
    books.append([1, 'The Intelligent Investor', 'Benjamin Graham', '9780060555665', 'Stocks/Investing', 'stocks, investing, finance', 'Library Block A', 2, 'F-12', 5, 5])
    books.append([2, 'Common Stocks and Uncommon Profits', 'Philip Fisher', '9780471445500', 'Stocks/Investing', 'stocks, profits, investing', 'Library Block A', 2, 'F-14', 3, 3])
    books.append([3, 'One Up On Wall Street', 'Peter Lynch', '9780743200400', 'Stocks/Investing', 'stocks, wall street', 'Library Block A', 2, 'F-15', 2, 0])
    books.append([4, 'Rich Dad Poor Dad', 'Robert Kiyosaki', '9781612681139', 'Finance', 'finance, money, investing', 'Library Block A', 2, 'F-10', 10, 4])
    
    # Generate remaining to reach 100
    for i in range(5, 101):
        cat = random.choice(categories)
        title = f"{cat} Principles Volume {i}"
        author = f"Author {i}"
        isbn = f"97810000{i:04d}"
        keywords = f"{cat.lower().replace('/', ', ')}, textbook, principles"
        building = "Library Block A"
        floor = random.randint(1, 4)
        shelf = f"{cat[0]}-{random.randint(1,20)}"
        total = random.randint(2, 10)
        avail = random.randint(0, total)
        books.append([i, title, author, isbn, cat, keywords, building, floor, shelf, total, avail])
        
    with open(os.path.join(MOCK_DIR, 'library_books.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'author', 'isbn', 'category', 'keywords', 'building', 'floor', 'shelf', 'total_copies', 'available_copies'])
        writer.writerows(books)

def generate_users_students():
    users = [
        [1, 'student1@university.edu', 'hashed_pass_123', 'Student'],
        [2, 'student2@university.edu', 'hashed_pass_123', 'Student']
    ]
    
    students = [
        [1, 'REG1001', 'Rahul Sharma', 8.5, 8.2, 'CSE', 5, 0, 2027],
        [2, 'REG1002', 'Priya Singh', 7.9, 7.8, 'ECE', 5, 1, 2027]
    ]
    
    with open(os.path.join(MOCK_DIR, 'users.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'email', 'password_hash', 'role'])
        writer.writerows(users)
        
    with open(os.path.join(MOCK_DIR, 'students.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['student_id', 'registration_number', 'name', 'cgpa', 'tgpa', 'branch', 'semester', 'backlogs', 'graduation_year'])
        writer.writerows(students)

def generate_academic():
    subjects = [
        ['CSE301', 'Database Management Systems', 4, 5, 'Intro to DB, ER Models, SQL...', 'Understand relational models.'],
        ['CSE302', 'Operating Systems', 4, 5, 'Processes, Threads, Memory...', 'Understand OS architecture.'],
        ['CSE303', 'Computer Networks', 3, 5, 'OSI, TCP/IP, Routing...', 'Understand network layers.'],
        ['CSE304', 'Artificial Intelligence', 4, 5, 'Search, ML, NLP...', 'Build basic AI agents.']
    ]
    
    faculty = [
        [1, 'Dr. Anil Kumar', 'CSE'],
        [2, 'Dr. Sunita Verma', 'CSE'],
        [3, 'Prof. Rakesh Gupta', 'CSE']
    ]
    
    with open(os.path.join(MOCK_DIR, 'subjects.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['subject_code', 'name', 'credits', 'semester', 'syllabus', 'course_outcomes'])
        writer.writerows(subjects)
        
    with open(os.path.join(MOCK_DIR, 'faculty.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['faculty_id', 'name', 'department'])
        writer.writerows(faculty)
        
def generate_attendance_exams():
    att = [
        [1, 1, 'CSE301', 42, 50],
        [2, 1, 'CSE302', 35, 45],
        [3, 1, 'CSE303', 40, 50],
        [4, 1, 'CSE304', 45, 50]
    ]
    
    exams = [
        [1, 1, 'CSE301', '2026-09-15', '10:00:00', 'Block 34, Hall 204'],
        [2, 1, 'CSE302', '2026-09-18', '14:00:00', 'Block 34, Hall 205']
    ]
    
    with open(os.path.join(MOCK_DIR, 'attendance.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'student_id', 'subject_code', 'attended_classes', 'total_classes'])
        writer.writerows(att)
        
    with open(os.path.join(MOCK_DIR, 'exams.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'student_id', 'subject_code', 'date', 'time', 'venue'])
        writer.writerows(exams)

def generate_fees_messages():
    fees = [
        [1, 1, 'SEMESTER_FEE', 60000.0, 40000.0, '2026-09-10'],
        [2, 1, 'RESIDENTIAL_FEE', 40000.0, 33000.0, '2026-09-10'],
        [3, 1, 'EXAMINATION_FEE', 1500.0, 0.0, '2026-09-10']
    ]
    
    msgs = [
        [1, 'Placement', 'TCS Placement Drive', 'TCS is visiting for SDE role on 28 Aug...', 'placement, tcs, sde', 'Placement Cell', 'High', '2026-08-25 10:00:00'],
        [2, 'Placement', 'Infosys Recruitment Drive', 'Infosys drive on 26 Aug...', 'placement, infosys', 'Placement Cell', 'Normal', '2026-08-20 10:00:00'],
        [3, 'Exam', 'Mid-Term Schedule', 'Mid terms starting from 15 Sep...', 'exam, mid-term, datesheet', 'Examination', 'High', '2026-08-27 10:00:00']
    ]
    
    with open(os.path.join(MOCK_DIR, 'fees.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'student_id', 'category', 'total_amount', 'paid_amount', 'due_date'])
        writer.writerows(fees)
        
    with open(os.path.join(MOCK_DIR, 'messages.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['message_id', 'category', 'title', 'content', 'tags', 'department', 'priority', 'published_at'])
        writer.writerows(msgs)

def generate_grading():
    rules = [
        [1, 'O', 90.0],
        [2, 'A+', 80.0],
        [3, 'A', 70.0],
        [4, 'B+', 60.0],
        [5, 'B', 50.0]
    ]
    with open(os.path.join(MOCK_DIR, 'grading_rules.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'grade', 'min_percentage'])
        writer.writerows(rules)

def main():
    print("Generating Mock Data...")
    generate_books()
    generate_users_students()
    generate_academic()
    generate_attendance_exams()
    generate_fees_messages()
    generate_grading()
    
    empty_files = {
        'faculty_leave': ['leave_id', 'faculty_id', 'date'],
        'timetable': ['id', 'student_id', 'subject_code', 'faculty_id', 'day', 'start_time', 'end_time', 'room', 'section'],
        'placement_drives': ['id', 'company', 'role', 'min_cgpa', 'min_tgpa', 'allowed_branches', 'deadline'],
        'placement_registrations': ['id', 'student_id', 'drive_id', 'status'],
        'leaves': ['id', 'student_id', 'type', 'from_date', 'to_date', 'reason', 'status'],
        'rms_categories': ['id', 'name', 'parent_id'],
        'rms_requests': ['id', 'student_id', 'category_id', 'description', 'status'],
        'student_marks': ['id', 'student_id', 'subject_code', 'ca1', 'ca2', 'mid_term', 'end_term']
    }
                   
    for filename, headers in empty_files.items():
        with open(os.path.join(MOCK_DIR, f"{filename}.csv"), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
    print("Mock Data Generated.")

if __name__ == '__main__':
    main()
