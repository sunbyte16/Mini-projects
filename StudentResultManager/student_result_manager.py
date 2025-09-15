class StudentResultManager:
    def __init__(self):
        self.students = {}

    def add_student(self, name):
        if name not in self.students:
            self.students[name] = {}
            return True
        return False

    def add_marks(self, name, subject, marks):
        if name in self.students:
            self.students[name][subject] = marks
            return True
        return False

    def calculate_total(self, name):
        if name in self.students and self.students[name]:
            return sum(self.students[name].values())
        return 0

    def calculate_average(self, name):
        if name in self.students and self.students[name]:
            return self.calculate_total(name) / len(self.students[name])
        return 0

    def calculate_grade(self, average):
        if average >= 90:
            return 'A+'
        elif average >= 80:
            return 'A'
        elif average >= 70:
            return 'B'
        elif average >= 60:
            return 'C'
        elif average >= 50:
            return 'D'
        else:
            return 'F'

    def generate_report(self, name):
        if name in self.students:
            total = self.calculate_total(name)
            average = self.calculate_average(name)
            grade = self.calculate_grade(average)
            
            print(f"\n--- Student Report ---")
            print(f"Name: {name}")
            print("\nSubject-wise Marks:")
            for subject, marks in self.students[name].items():
                print(f"{subject}: {marks}")
            print(f"\nTotal Marks: {total}")
            print(f"Average: {average:.2f}")
            print(f"Grade: {grade}")
            print("----------------------")
        else:
            print("Student not found!")

def main():
    srm = StudentResultManager()
    
    while True:
        print("\nStudent Result Manager")
        print("1. Add Student")
        print("2. Add Marks")
        print("3. View Report")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            name = input("Enter student name: ")
            if srm.add_student(name):
                print(f"Student {name} added successfully!")
            else:
                print("Student already exists!")
                
        elif choice == '2':
            name = input("Enter student name: ")
            if name in srm.students:
                subject = input("Enter subject name: ")
                try:
                    marks = float(input("Enter marks (0-100): "))
                    if 0 <= marks <= 100:
                        srm.add_marks(name, subject, marks)
                        print("Marks added successfully!")
                    else:
                        print("Marks should be between 0 and 100!")
                except ValueError:
                    print("Please enter a valid number!")
            else:
                print("Student not found!")
                
        elif choice == '3':
            name = input("Enter student name: ")
            srm.generate_report(name)
            
        elif choice == '4':
            print("Thank you for using Student Result Manager!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
