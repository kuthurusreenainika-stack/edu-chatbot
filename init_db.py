import sqlite3
from datetime import datetime


def init():
    with sqlite3.connect("campus.db") as conn:
        c = conn.cursor()

        # Drop tables if they exist
        c.executescript("""
        DROP TABLE IF EXISTS schedules;
        DROP TABLE IF EXISTS dining;
        DROP TABLE IF EXISTS library;
        DROP TABLE IF EXISTS admin;
        DROP TABLE IF EXISTS departments;
        DROP TABLE IF EXISTS courses;
        DROP TABLE IF EXISTS staff;
        DROP TABLE IF EXISTS events;
        DROP TABLE IF EXISTS students;
        DROP TABLE IF EXISTS enrollments;
        DROP TABLE IF EXISTS announcements;
        DROP TABLE IF EXISTS office_hours;
        DROP TABLE IF EXISTS transport;
        DROP TABLE IF EXISTS feedback;
        """)

        # Create tables
        c.execute("""CREATE TABLE schedules (
            id INTEGER PRIMARY KEY, building TEXT, room TEXT,
            event TEXT, day TEXT, start_time TEXT, end_time TEXT
        )""")

        c.execute("""CREATE TABLE dining (
            id INTEGER PRIMARY KEY, location TEXT, hours TEXT,
            menu TEXT, notes TEXT
        )""")

        c.execute("""CREATE TABLE library (
            id INTEGER PRIMARY KEY, service TEXT, hours TEXT,
            contact TEXT, notes TEXT
        )""")

        c.execute("""CREATE TABLE admin (
            id INTEGER PRIMARY KEY, topic TEXT, description TEXT,
            contact TEXT, url TEXT
        )""")

        c.execute("""CREATE TABLE departments (
            id INTEGER PRIMARY KEY, name TEXT, head TEXT, contact TEXT
        )""")

        c.execute("""CREATE TABLE courses (
            id INTEGER PRIMARY KEY, name TEXT, department_id INTEGER,
            credits INTEGER, FOREIGN KEY(department_id) REFERENCES departments(id)
        )""")

        c.execute("""CREATE TABLE staff (
            id INTEGER PRIMARY KEY, name TEXT, role TEXT,
            department_id INTEGER, email TEXT,
            FOREIGN KEY(department_id) REFERENCES departments(id)
        )""")

        c.execute("""CREATE TABLE events (
            id INTEGER PRIMARY KEY, name TEXT, date TEXT,
            location TEXT, description TEXT
        )""")

        c.execute("""CREATE TABLE students (
            id INTEGER PRIMARY KEY, name TEXT, email TEXT,
            department_id INTEGER, year INTEGER,
            FOREIGN KEY(department_id) REFERENCES departments(id)
        )""")

        c.execute("""CREATE TABLE enrollments (
            id INTEGER PRIMARY KEY, student_id INTEGER,
            course_id INTEGER, grade TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )""")

        c.execute("""CREATE TABLE announcements (
            id INTEGER PRIMARY KEY, title TEXT, content TEXT, date TEXT
        )""")

        c.execute("""CREATE TABLE office_hours (
            id INTEGER PRIMARY KEY, staff_id INTEGER, day TEXT,
            start_time TEXT, end_time TEXT, location TEXT,
            FOREIGN KEY(staff_id) REFERENCES staff(id)
        )""")

        c.execute("""CREATE TABLE transport (
            id INTEGER PRIMARY KEY, route_name TEXT, stops TEXT,
            start_time TEXT, end_time TEXT, frequency TEXT
        )""")

        c.execute("""CREATE TABLE feedback (
            id INTEGER PRIMARY KEY, student_id INTEGER, category TEXT,
            message TEXT, date TEXT, FOREIGN KEY(student_id) REFERENCES students(id)
        )""")

        # --- Sample Data ---
        schedules = [
            ("Main Hall", "101", "Linear Algebra Lecture", "Mon", "09:00", "10:30"),
            ("Science Block", "210", "Organic Chemistry Lab", "Tue", "11:00", "13:00"),
            ("Engineering Block", "305", "Programming Basics", "Wed", "10:00", "11:30"),
            ("Auditorium", "001", "Guest Lecture on AI", "Thu", "14:00", "16:00")
        ]
        c.executemany(
            "INSERT INTO schedules (building,room,event,day,start_time,end_time) VALUES (?,?,?,?,?,?)", schedules)

        dining = [
            ("North Canteen", "07:30-20:00",
             "Breakfast: Idli/Vada; Lunch: Rice, Dal; Dinner: Chapati & Veg Curry", "Veg options available"),
            ("South Canteen", "10:00-22:00",
             "Snacks, Coffee, Burgers, Sandwiches", "Accepts student card"),
            ("East Canteen", "08:00-21:00",
             "South Indian, North Indian, Salads", "Offers student discounts")
        ]
        c.executemany(
            "INSERT INTO dining (location,hours,menu,notes) VALUES (?,?,?,?)", dining)

        library = [
            ("Borrowing", "08:00-22:00", "library@campus.edu",
             "Return books within 2 weeks"),
            ("Study Rooms", "08:00-20:00", "rooms@campus.edu", "Book via portal"),
            ("Research Section", "09:00-18:00", "research@campus.edu",
             "Access restricted to research students")
        ]
        c.executemany(
            "INSERT INTO library (service,hours,contact,notes) VALUES (?,?,?,?)", library)

        admin = [
            ("Transcript Request", "Fill online form; 5 working days",
             "registry@campus.edu", "https://campus.edu/transcripts"),
            ("Fee Payment", "Pay semester fees online or at admin office",
             "finance@campus.edu", "https://campus.edu/fees")
        ]
        c.executemany(
            "INSERT INTO admin (topic,description,contact,url) VALUES (?,?,?,?)", admin)

        departments = [
            ("Mathematics", "Dr. Ramanujan", "math@campus.edu"),
            ("Chemistry", "Dr. Curie", "chem@campus.edu"),
            ("Computer Science", "Dr. Turing", "cs@campus.edu")
        ]
        c.executemany(
            "INSERT INTO departments (name,head,contact) VALUES (?,?,?)", departments)

        courses = [
            ("Linear Algebra", 1, 3),
            ("Organic Chemistry", 2, 4),
            ("Programming Basics", 3, 3),
            ("Data Structures", 3, 4)
        ]
        c.executemany(
            "INSERT INTO courses (name,department_id,credits) VALUES (?,?,?)", courses)

        staff = [
            ("Dr. Euler", "Professor", 1, "euler@campus.edu"),
            ("Dr. Marie", "Lab Instructor", 2, "marie@campus.edu"),
            ("Dr. Ada", "Assistant Professor", 3, "ada@campus.edu")
        ]
        c.executemany(
            "INSERT INTO staff (name,role,department_id,email) VALUES (?,?,?,?)", staff)

        events = [
            ("Science Fair", "2025-10-05", "Auditorium",
             "Annual student science fair"),
            ("Cultural Fest", "2025-12-01",
             "Main Hall", "Music, Dance, Drama events"),
            ("Hackathon", "2025-11-20", "Computer Lab", "24-hour coding event")
        ]
        c.executemany(
            "INSERT INTO events (name,date,location,description) VALUES (?,?,?,?)", events)

        students = [
            ("Alice", "alice@campus.edu", 1, 2),
            ("Bob", "bob@campus.edu", 2, 1),
            ("Charlie", "charlie@campus.edu", 3, 3),
            ("Diana", "diana@campus.edu", 3, 2)
        ]
        c.executemany(
            "INSERT INTO students (name,email,department_id,year) VALUES (?,?,?,?)", students)

        enrollments = [
            (1, 1, "A"),
            (2, 2, "B"),
            (3, 3, None),
            (4, 4, None)
        ]
        c.executemany(
            "INSERT INTO enrollments (student_id,course_id,grade) VALUES (?,?,?)", enrollments)

        announcements = [
            ("Maintenance Alert", "Library closed on 2025-09-15", "2025-09-13"),
            ("Guest Lecture", "Prof. Smith will give a talk on AI", "2025-09-14"),
            ("Holiday Notice", "Campus closed on 2025-12-25", "2025-12-20")
        ]
        c.executemany(
            "INSERT INTO announcements (title,content,date) VALUES (?,?,?)", announcements)

        office_hours = [
            (1, "Mon", "14:00", "16:00", "Math Dept Room 101"),
            (2, "Tue", "10:00", "12:00", "Chem Dept Room 210"),
            (3, "Wed", "15:00", "17:00", "CS Dept Room 305")
        ]
        c.executemany(
            "INSERT INTO office_hours (staff_id,day,start_time,end_time,location) VALUES (?,?,?,?,?)", office_hours)

        transport = [
            ("Route A", "Gate1, Library, Science Block",
             "08:00", "18:00", "Every 30 min"),
            ("Route B", "Gate2, Main Hall, Dorms",
             "09:00", "20:00", "Every 45 min"),
            ("Route C", "Dorms, Canteens, CS Block",
             "07:30", "19:00", "Every 20 min")
        ]
        c.executemany(
            "INSERT INTO transport (route_name,stops,start_time,end_time,frequency) VALUES (?,?,?,?,?)", transport)

        feedbacks = [
            (1, "Library", "Need more study tables", "2025-09-12"),
            (2, "Canteen", "More vegetarian options", "2025-09-13"),
            (3, "Courses", "Add advanced programming courses", "2025-09-14")
        ]
        c.executemany(
            "INSERT INTO feedback (student_id,category,message,date) VALUES (?,?,?,?)", feedbacks)

    print(
        f"✅ campus.db created with extended sample data on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

# Helper function to query today's schedule


def today_schedule(day):
    with sqlite3.connect("campus.db") as conn:
        c = conn.cursor()
        c.execute(
            "SELECT building, room, event, start_time, end_time FROM schedules WHERE day=?", (day,))
        results = c.fetchall()
        print(f"\n📅 Schedule for {day}:")
        for r in results:
            print(
                f"Building: {r[0]}, Room: {r[1]}, Event: {r[2]}, {r[3]}-{r[4]}")


if __name__ == "__main__":
    init()
    today_schedule("Mon")
    today_schedule("Tue")
