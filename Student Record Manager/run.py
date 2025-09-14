#!/usr/bin/env python3
"""
Main entry point for Student Record Manager
Run this file to start the application
"""

import sys
import os

def main():
    """Main entry point"""
    print("🎓 Student Record Manager - Main Entry Point")
    print("=" * 50)
    print("Choose your preferred version:")
    print("1. Full Application (student_manager.py)")
    print("2. Simple Interactive (simple_student_manager.py)")
    print("3. Quick Demo (quick_demo.py)")
    print("4. Generate Demo Data (demo_data.py)")
    print("0. Exit")
    print("=" * 50)
    
    while True:
        try:
            choice = input("\nEnter your choice (0-4): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                sys.exit(0)
            elif choice == "1":
                print("\n🚀 Starting Full Application...")
                os.system("python student_manager.py")
                break
            elif choice == "2":
                print("\n🎯 Starting Simple Interactive Version...")
                os.system("python simple_student_manager.py")
                break
            elif choice == "3":
                print("\n🎬 Starting Quick Demo...")
                os.system("python quick_demo.py")
                break
            elif choice == "4":
                print("\n🎲 Starting Demo Data Generator...")
                os.system("python demo_data.py")
                break
            else:
                print("❌ Invalid choice! Please enter 0-4.")
        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
