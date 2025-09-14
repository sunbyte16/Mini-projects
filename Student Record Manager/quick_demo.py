#!/usr/bin/env python3
"""
Quick Demo - Student Record Manager
Shows immediate input/output examples
"""

import json
import os

def quick_demo():
    """Run a quick demo showing input/output"""
    print("🎓 QUICK DEMO - STUDENT RECORD MANAGER")
    print("="*50)
    
    # Initialize empty database
    students = []
    
    print("\n📝 DEMO: Adding Students")
    print("-" * 30)
    
    # Demo 1: Add first student
    print("Adding student 1...")
    student1 = {
        'student_id': 'S001',
        'name': 'Sunil Sharma',
        'age': 20,
        'grade': 'A',
        'email': 'sunil.sharma@email.com'
    }
    students.append(student1)
    print("✅ OUTPUT: Student added successfully!")
    print(f"   Student ID: {student1['student_id']}")
    print(f"   Name: {student1['name']}")
    print(f"   Age: {student1['age']}")
    print(f"   Grade: {student1['grade']}")
    print(f"   Email: {student1['email']}")
    
    # Demo 2: Add second student
    print("\nAdding student 2...")
    student2 = {
        'student_id': 'S002',
        'name': 'Jane Smith',
        'age': 19,
        'grade': 'B+',
        'email': 'jane.smith@email.com'
    }
    students.append(student2)
    print("✅ OUTPUT: Student added successfully!")
    print(f"   Student ID: {student2['student_id']}")
    print(f"   Name: {student2['name']}")
    print(f"   Age: {student2['age']}")
    print(f"   Grade: {student2['grade']}")
    print(f"   Email: {student2['email']}")
    
    # Demo 3: View all students
    print("\n📚 DEMO: Viewing All Students")
    print("-" * 30)
    print("✅ OUTPUT: All student records:")
    print("="*80)
    print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Grade':<10} {'Email':<25}")
    print("-"*80)
    for student in students:
        print(f"{student['student_id']:<10} {student['name']:<20} {student['age']:<5} {student['grade']:<10} {student['email']:<25}")
    print("="*80)
    
    # Demo 4: Search student
    print("\n🔍 DEMO: Searching for Student")
    print("-" * 30)
    search_term = "Sunil"
    print(f"Searching for: '{search_term}'")
    
    matches = [s for s in students if search_term.lower() in s['name'].lower()]
    print("✅ OUTPUT: Search results:")
    if matches:
        for student in matches:
            print(f"   Found: {student['name']} (ID: {student['student_id']})")
    else:
        print("   No matches found")
    
    # Demo 5: Update student
    print("\n✏️ DEMO: Updating Student")
    print("-" * 30)
    student_id = "S001"
    student = next((s for s in students if s['student_id'] == student_id), None)
    
    if student:
        print(f"Updating student: {student['name']}")
        student['grade'] = 'A+'
        student['age'] = 21
        print("✅ OUTPUT: Student updated successfully!")
        print(f"   Updated Grade: {student['grade']}")
        print(f"   Updated Age: {student['age']}")
    
    # Demo 6: Delete student
    print("\n🗑️ DEMO: Deleting Student")
    print("-" * 30)
    student_id = "S002"
    student = next((s for s in students if s['student_id'] == student_id), None)
    
    if student:
        print(f"Deleting student: {student['name']}")
        students = [s for s in students if s['student_id'] != student_id]
        print("✅ OUTPUT: Student deleted successfully!")
        print(f"   Remaining students: {len(students)}")
    
    # Final view
    print("\n📚 FINAL DEMO: Updated Student List")
    print("-" * 30)
    print("✅ OUTPUT: Current student records:")
    print("="*80)
    print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Grade':<10} {'Email':<25}")
    print("-"*80)
    for student in students:
        print(f"{student['student_id']:<10} {student['name']:<20} {student['age']:<5} {student['grade']:<10} {student['email']:<25}")
    print("="*80)
    
    # Save demo data
    with open("demo_students.json", 'w') as file:
        json.dump(students, file, indent=2)
    print(f"\n💾 Demo data saved to 'demo_students.json'")
    
    print("\n🎯 DEMO COMPLETE!")
    print("This shows how the program takes input and provides immediate output.")
    print("Run 'python simple_student_manager.py' for the interactive version!")

if __name__ == "__main__":
    quick_demo()
