import json
import os
from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime, date, timedelta

@dataclass
class Student:
    id: str
    name: str
    email: str
    class_name: str

@dataclass
class AttendanceRecord:
    student_id: str
    date: str
    status: str  # 'present', 'absent', 'late', 'excused'

class AttendanceSystem:
    def __init__(self):
        self.students: Dict[str, Student] = {}
        self.attendance: Dict[str, Dict[str, str]] = {}  # student_id -> {date -> status}
        self.load_data()
    
    def load_data(self):
        if os.path.exists('students.json'):
            with open('students.json', 'r') as f:
                data = json.load(f)
                self.students = {k: Student(**v) for k, v in data.items()}
        
        if os.path.exists('attendance.json'):
            with open('attendance.json', 'r') as f:
                self.attendance = json.load(f)
    
    def save_data(self):
        with open('students.json', 'w') as f:
            json.dump({k: v.__dict__ for k, v in self.students.items()}, f, indent=2)
        
        with open('attendance.json', 'w') as f:
            json.dump(self.attendance, f, indent=2)
    
    def add_student(self, name: str, email: str, class_name: str) -> str:
        student_id = f"S{len(self.students) + 1:03d}"
        self.students[student_id] = Student(student_id, name, email, class_name)
        self.attendance[student_id] = {}
        self.save_data()
        return student_id
    
    def record_attendance(self, student_id: str, date_str: str, status: str) -> bool:
        if student_id not in self.students or status not in ["present", "absent", "late", "excused"]:
            return False
        
        if student_id not in self.attendance:
            self.attendance[student_id] = {}
        
        self.attendance[student_id][date_str] = status
        self.save_data()
        return True
    
    def get_student_attendance(self, student_id: str) -> Dict[str, str]:
        return self.attendance.get(student_id, {})
    
    def get_class_attendance(self, class_name: str, date_str: str = None) -> List[dict]:
        result = []
        for student in self.students.values():
            if student.class_name != class_name:
                continue
                
            records = self.get_student_attendance(student.id)
            attendance_data = {
                'student_id': student.id,
                'name': student.name,
                'present': 0,
                'absent': 0,
                'late': 0,
                'excused': 0,
                'attendance_rate': 0
            }
            
            for date_key, status in records.items():
                if date_str and date_key != date_str:
                    continue
                attendance_data[status] += 1
            
            total = attendance_data['present'] + attendance_data['absent'] + attendance_data['late']
            if total > 0:
                attendance_data['attendance_rate'] = (
                    (attendance_data['present'] + 0.5 * attendance_data['late']) / total * 100
                )
            
            result.append(attendance_data)
        
        return result

def display_menu():
    print("\n=== Student Attendance System ===")
    print("1. Add Student")
    print("2. Record Attendance")
    print("3. View Attendance")
    print("4. Generate Report")
    print("5. Exit")

def display_attendance(attendance_data: List[dict], show_details: bool = False):
    if not attendance_data:
        print("No attendance records found.")
        return
    
    print("\n{:<8} {:<20} {:<8} {:<8} {:<8} {:<8} {:<10}".format(
        "ID", "Name", "Present", "Absent", "Late", "Excused", "Rate"))
    print("-" * 80)
    
    for data in sorted(attendance_data, key=lambda x: x['attendance_rate'], reverse=True):
        print("{:<8} {:<20} {:<8} {:<8} {:<8} {:<8} {:<10.1f}%".format(
            data['student_id'],
            data['name'][:19],
            data['present'],
            data['absent'],
            data['late'],
            data['excused'],
            data['attendance_rate']
        ))

def main():
    system = AttendanceSystem()
    
    # Add sample data if empty
    if not system.students:
        print("Initializing with sample data...")
        classes = ["10A", "10B", "11A", "11B", "12A"]
        names = ["John Smith", "Jane Doe", "Michael Johnson", "Emily Davis", "David Wilson"]
        
        for i, name in enumerate(names, 1):
            class_name = classes[i % len(classes)]
            email = f"{name.split()[0].lower()}.{name.split()[-1].lower()}@school.edu"
            system.add_student(name, email, class_name)
            
            # Add sample attendance for the past 7 days
            for days_ago in range(7):
                date_str = (date.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
                status = ["present", "absent", "late", "excused"][(i + days_ago) % 4]
                system.record_attendance(f"S{i:03d}", date_str, status)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':  # Add Student
            print("\n=== Add New Student ===")
            name = input("Full Name: ").strip()
            email = input("Email: ").strip()
            class_name = input("Class: ").strip().upper()
            
            if not all([name, email, class_name]):
                print("All fields are required.")
                continue
            
            student_id = system.add_student(name, email, class_name)
            print(f"\n✅ Student added successfully! ID: {student_id}")
        
        elif choice == '2':  # Record Attendance
            print("\n=== Record Attendance ===")
            date_str = input("Date (YYYY-MM-DD, leave empty for today): ").strip()
            if not date_str:
                date_str = date.today().strftime("%Y-%m-%d")
            
            print(f"\nRecording attendance for {date_str}")
            print("Status codes: P=Present, A=Absent, L=Late, E=Excused")
            
            for student_id, student in system.students.items():
                while True:
                    status = input(f"{student.name} ({student.class_name}): ").strip().upper()
                    
                    if not status:  # Default to present if no input
                        status = 'P'
                    
                    status_map = {'P': 'present', 'A': 'absent', 'L': 'late', 'E': 'excused'}
                    if status in status_map:
                        system.record_attendance(student_id, date_str, status_map[status])
                        break
                    else:
                        print("Invalid status. Please enter P, A, L, or E.")
            
            print(f"\n✅ Attendance recorded for {len(system.students)} students")
        
        elif choice == '3':  # View Attendance
            print("\n=== View Attendance ===")
            class_name = input("Enter class (leave empty for all): ").strip().upper()
            date_str = input("Date (YYYY-MM-DD, leave empty for all): ").strip()
            
            if class_name:
                attendance_data = system.get_class_attendance(class_name, date_str if date_str else None)
            else:
                attendance_data = []
                for student in system.students.values():
                    class_data = system.get_class_attendance(student.class_name, date_str if date_str else None)
                    attendance_data.extend(class_data)
            
            display_attendance(attendance_data)
        
        elif choice == '4':  # Generate Report
            print("\n=== Generate Report ===")
            class_name = input("Enter class (leave empty for all): ").strip().upper()
            
            if class_name:
                attendance_data = system.get_class_attendance(class_name)
            else:
                attendance_data = []
                for student in system.students.values():
                    class_data = system.get_class_attendance(student.class_name)
                    attendance_data.extend(class_data)
            
            print("\n=== Attendance Report ===")
            display_attendance(attendance_data)
            
            # Export to file
            if input("\nExport to file? (y/n): ").strip().lower() == 'y':
                filename = f"attendance_report_{date.today().strftime('%Y%m%d')}.txt"
                with open(filename, 'w') as f:
                    f.write("=== Attendance Report ===\n")
                    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    if class_name:
                        f.write(f"Class: {class_name}\n")
                    f.write("-" * 80 + "\n")
                    f.write("{:<8} {:<20} {:<8} {:<8} {:<8} {:<8} {:<10}\n".format(
                        "ID", "Name", "Present", "Absent", "Late", "Excused", "Rate"))
                    f.write("-" * 80 + "\n")
                    
                    for data in sorted(attendance_data, key=lambda x: x['attendance_rate'], reverse=True):
                        f.write("{:<8} {:<20} {:<8} {:<8} {:<8} {:<8} {:<10.1f}%\n".format(
                            data['student_id'],
                            data['name'][:19],
                            data['present'],
                            data['absent'],
                            data['late'],
                            data['excused'],
                            data['attendance_rate']
                        ))
                
                print(f"\n✅ Report saved as {filename}")
        
        elif choice == '5':  # Exit
            print("\nThank you for using the Student Attendance System!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
