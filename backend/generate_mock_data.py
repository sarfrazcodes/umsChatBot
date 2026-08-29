import os
import csv
import random
from datetime import datetime, timedelta

MOCK_DIR = os.path.join(os.path.dirname(__file__), "mock_data")
os.makedirs(MOCK_DIR, exist_ok=True)

def generate_books():
    categories = ['Programming', 'Data Structures', 'Algorithms', 'Database', 'AI/ML', 'Cybersecurity', 'Web Development', 'Finance', 'Stocks/Investing', 'Mathematics', 'Physics', 'Business', 'Entrepreneurship', 'General Reading']
    
    books = []
    books.append([1, 'The Intelligent Investor', 'Benjamin Graham', '9780060555665', 'Stocks/Investing', 'stocks, investing, finance', 'Library Block A', 2, 'F-12', 5, 5])
    books.append([2, 'Common Stocks and Uncommon Profits', 'Philip Fisher', '9780471445500', 'Stocks/Investing', 'stocks, profits, investing', 'Library Block A', 2, 'F-14', 3, 3])
    books.append([3, 'One Up On Wall Street', 'Peter Lynch', '9780743200400', 'Stocks/Investing', 'stocks, wall street', 'Library Block A', 2, 'F-15', 2, 0])
    books.append([4, 'Rich Dad Poor Dad', 'Robert Kiyosaki', '9781612681139', 'Finance', 'finance, money, investing', 'Library Block A', 2, 'F-10', 10, 4])
    
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
        [1, 'sarfraz@university.edu', 'password123', 'Student'],
        [2, 'student2@university.edu', 'password123', 'Student']
    ]
    
    students = [
        [1, '12505649', 'Sarfraz', 8.72, 8.5, 'CSE', 3, 0, 2027],
        [2, 'REG1002', 'Priya Singh', 7.9, 7.8, 'ECE', 3, 1, 2027]
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
        ['CSE316', 'Operating Systems', 4, 3, 'Processes, Threads, Memory...', 'Understand OS architecture.'],
        ['INT221', 'Full Stack Web Dev', 4, 3, 'HTML, CSS, JS, React...', 'Build full stack web apps.'],
        ['CSE320', 'AI & Machine Learning', 4, 3, 'Search, ML, NLP...', 'Build basic AI agents.'],
        ['MTH302', 'Engineering Mathematics', 4, 3, 'Calculus, Algebra...', 'Solve engineering mathematical problems.'],
        ['PEL136', 'English Advance', 2, 3, 'Advanced English communication skills...', 'Enhance verbal and written communication.'],
        ['CSE205', 'Data Structures and Algorithms', 4, 3, 'Arrays, Trees, Graphs, Sorting...', 'Implement efficient algorithms.'],
        ['INT205', 'Object Oriented Programming', 4, 3, 'Classes, Inheritance, Polymorphism...', 'Master OOP concepts.'],
        ['CSE276', 'AI & ML Foundation', 3, 3, 'Intro to AI, logic, simple regression...', 'Understand foundations of AI.'],
        ['CSE306', 'Computer Networks', 4, 3, 'OSI model, TCP/IP, Routing protocols...', 'Understand network layers and protocols.']
    ]
    
    faculty = [
        [1, 'Dr. Anil Kumar', 'CSE'],
        [2, 'Dr. Sunita Verma', 'CSE'],
        [3, 'Prof. Rakesh Gupta', 'CSE'],
        [4, 'Dr. Vikram Singh', 'MTH']
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
        [1, 1, 'CSE316', 35, 40], # 87.5%
        [2, 1, 'INT221', 42, 47], # 89.4%
        [3, 1, 'CSE320', 33, 42], # 78.5%
        [4, 1, 'MTH302', 35, 42], # 83.3%
        [5, 1, 'PEL136', 18, 20], # 90.0%
        [6, 1, 'CSE205', 38, 40], # 95.0%
        [7, 1, 'INT205', 30, 40], # 75.0%
        [8, 1, 'CSE276', 25, 30], # 83.3%
        [9, 1, 'CSE306', 36, 40]  # 90.0%
    ]
    
    exams = [
        [1, 1, 'CSE316', '2026-09-15', '10:00:00', 'Block 34, Hall 204'],
        [2, 1, 'INT221', '2026-09-18', '14:00:00', 'Block 34, Hall 205'],
        [3, 1, 'CSE320', '2026-09-20', '10:00:00', 'Block 14, Hall 101'],
        [4, 1, 'MTH302', '2026-09-22', '14:00:00', 'Block 10, Hall 110'],
        [5, 1, 'PEL136', '2026-09-24', '10:00:00', 'Block 33, Hall 102'],
        [6, 1, 'CSE205', '2026-09-26', '14:00:00', 'Block 34, Hall 204'],
        [7, 1, 'INT205', '2026-09-28', '10:00:00', 'Block 32, Hall 201'],
        [8, 1, 'CSE276', '2026-09-30', '14:00:00', 'Block 14, Hall 102'],
        [9, 1, 'CSE306', '2026-10-02', '10:00:00', 'Block 34, Hall 205']
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
        [1, 1, 'SEMESTER_FEE', 60000.0, 60000.0, '2026-09-10'],
        [2, 1, 'RESIDENTIAL_FEE', 40000.0, 30000.0, '2026-09-10'],
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

def generate_timetable():
    # Day mapping
    import calendar
    today = datetime.today()
    specific_day = calendar.day_name[today.weekday()]
    
    timetable = [
        # Mon29 schedule (used as current day for dynamic testing, but let's populate for the whole week)
        [1, 1, 'CSE316', 1, 'Monday', '09:00:00', '10:00:00', 'Block 14 - Room 302', 'K22'],
        [2, 1, 'INT221', 2, 'Monday', '10:00:00', '11:00:00', 'Block 32 - Lab 4', 'K22'],
        [3, 1, 'CSE320', 3, 'Monday', '11:00:00', '12:00:00', 'Block 34 - Room 201', 'K22'],
        [11, 1, 'PEL136', 4, 'Monday', '13:00:00', '14:00:00', 'Block 33 - Room 102', 'K22'],
        [12, 1, 'CSE205', 1, 'Monday', '14:00:00', '15:00:00', 'Block 34 - Room 204', 'K22'],
        
        [4, 1, 'MTH302', 4, 'Tuesday', '09:00:00', '10:00:00', 'Block 10 - Room 110', 'K22'],
        [13, 1, 'INT205', 2, 'Tuesday', '10:00:00', '11:00:00', 'Block 32 - Room 201', 'K22'],
        [14, 1, 'CSE276', 3, 'Tuesday', '11:00:00', '12:00:00', 'Block 14 - Room 102', 'K22'],
        [15, 1, 'CSE306', 1, 'Tuesday', '13:00:00', '14:00:00', 'Block 34 - Room 205', 'K22'],

        [5, 1, 'CSE316', 1, 'Wednesday', '11:00:00', '12:00:00', 'Block 14 - Lab 2', 'K22'],
        [16, 1, 'PEL136', 4, 'Wednesday', '13:00:00', '14:00:00', 'Block 33 - Room 102', 'K22'],
        [17, 1, 'CSE205', 1, 'Wednesday', '14:00:00', '15:00:00', 'Block 34 - Lab 204', 'K22'],

        [6, 1, 'CSE320', 3, 'Thursday', '09:00:00', '10:00:00', 'Block 34 - Room 201', 'K22'],
        [18, 1, 'INT205', 2, 'Thursday', '10:00:00', '11:00:00', 'Block 32 - Lab 201', 'K22'],
        [19, 1, 'CSE276', 3, 'Thursday', '11:00:00', '12:00:00', 'Block 14 - Room 102', 'K22'],

        [7, 1, 'INT221', 2, 'Friday', '10:00:00', '11:00:00', 'Block 32 - Lab 4', 'K22'],
        [20, 1, 'CSE306', 1, 'Friday', '13:00:00', '14:00:00', 'Block 34 - Room 205', 'K22'],
        [21, 1, 'MTH302', 4, 'Friday', '14:00:00', '15:00:00', 'Block 10 - Room 110', 'K22'],
    ]
    
    # Also add current day fallback just in case today is Saturday/Sunday
    timetable.append([8, 1, 'CSE316', 1, specific_day, '09:00:00', '10:00:00', 'Block 14 - Room 302', 'K22'])
    timetable.append([9, 1, 'INT221', 2, specific_day, '10:00:00', '11:00:00', 'Block 32 - Lab 4', 'K22'])
    timetable.append([10, 1, 'CSE320', 3, specific_day, '11:00:00', '12:00:00', 'Block 34 - Room 201', 'K22'])
    
    with open(os.path.join(MOCK_DIR, 'timetable.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'student_id', 'subject_code', 'faculty_id', 'day', 'start_time', 'end_time', 'room', 'section'])
        writer.writerows(timetable)

def generate_rms():
    rms_categories = [
        [1, 'IT Support', ''],
        [2, 'Hostel Maintenance', ''],
        [3, 'Wi-Fi Issue', 1],
        [4, 'Plumbing', 2],
        [5, 'Electrical', 2]
    ]
    rms_requests = [
        [1, 1, 3, 'Wi-Fi keeps dropping in my hostel room', 'Resolved'],
        [2, 1, 5, 'Ceiling fan is making loud noise', 'In Progress'],
        [3, 1, 4, 'Tap is leaking', 'Pending']
    ]
    
    with open(os.path.join(MOCK_DIR, 'rms_categories.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'parent_id'])
        writer.writerows(rms_categories)
        
    with open(os.path.join(MOCK_DIR, 'rms_requests.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'student_id', 'category_id', 'description', 'status'])
        writer.writerows(rms_requests)

def generate_others():
    faculty_leave = [
        [1, 2, datetime.today().strftime('%Y-%m-%d')] # Make Sunita Verma on leave today
    ]
    placement_drives = [
        [1, 'Amazon', 'SDE I', 8.0, 7.5, 'CSE,ECE', '2026-10-15'],
        [2, 'TCS', 'System Engineer', 6.0, 6.0, 'CSE,ECE,ME,CE', '2026-09-20'],
        [3, 'Google', 'Software Engineer', 8.5, 8.0, 'CSE', '2026-11-01']
    ]
    placement_registrations = [
        [1, 1, 1, 'Registered'],
        [2, 1, 2, 'Registered']
    ]
    leaves = [
        [1, 1, 'Hostel Leave', '2026-08-20', '2026-08-22', 'Going home', 'Approved'],
        [2, 1, 'Campus Pass', '2026-09-01', '2026-09-01', 'Medical checkup', 'Pending']
    ]
    student_marks = [
        [1, 1, 'CSE316', 25.0, 28.0, 35.0, 0.0],
        [2, 1, 'INT221', 28.0, 26.0, 38.0, 0.0],
        [3, 1, 'CSE320', 20.0, 22.0, 30.0, 0.0],
        [4, 1, 'MTH302', 26.0, 29.0, 33.0, 0.0],
        [5, 1, 'PEL136', 29.0, 30.0, 39.0, 0.0],
        [6, 1, 'CSE205', 25.0, 26.0, 37.0, 0.0],
        [7, 1, 'INT205', 22.0, 24.0, 32.0, 0.0],
        [8, 1, 'CSE276', 24.0, 25.0, 34.0, 0.0],
        [9, 1, 'CSE306', 27.0, 28.0, 36.0, 0.0]
    ]
    
    with open(os.path.join(MOCK_DIR, 'faculty_leave.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['leave_id', 'faculty_id', 'date'])
        writer.writerows(faculty_leave)
        
    with open(os.path.join(MOCK_DIR, 'placement_drives.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'company', 'role', 'min_cgpa', 'min_tgpa', 'allowed_branches', 'deadline'])
        writer.writerows(placement_drives)
        
    with open(os.path.join(MOCK_DIR, 'placement_registrations.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'student_id', 'drive_id', 'status'])
        writer.writerows(placement_registrations)
        
    with open(os.path.join(MOCK_DIR, 'leaves.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'student_id', 'type', 'from_date', 'to_date', 'reason', 'status'])
        writer.writerows(leaves)
        
    with open(os.path.join(MOCK_DIR, 'student_marks.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'student_id', 'subject_code', 'ca1', 'ca2', 'mid_term', 'end_term'])
        writer.writerows(student_marks)

def main():
    print("Generating Mock Data...")
    generate_books()
    generate_users_students()
    generate_academic()
    generate_attendance_exams()
    generate_fees_messages()
    generate_grading()
    generate_timetable()
    generate_rms()
    generate_others()
    print("Mock Data Generated.")

if __name__ == '__main__':
    main()
