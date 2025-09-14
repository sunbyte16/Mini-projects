#!/usr/bin/env python3
"""
Configuration file for Student Record Manager
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for Student Record Manager"""
    
    # Application settings
    APP_NAME = "Student Record Manager"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "Sunil Sharma"
    
    # File settings
    DEFAULT_JSON_FILE = "students.json"
    DEFAULT_CSV_FILE = "students.csv"
    DEMO_JSON_FILE = "demo_students.json"
    DEMO_CSV_FILE = "demo_students.csv"
    
    # Data validation settings
    MIN_AGE = 1
    MAX_AGE = 150
    REQUIRED_FIELDS = ['student_id', 'name', 'age', 'grade', 'email']
    
    # Display settings
    TABLE_WIDTH = 80
    MENU_WIDTH = 60
    
    # File formats
    SUPPORTED_FORMATS = ['json', 'csv']
    
    # Error messages
    ERROR_MESSAGES = {
        'duplicate_id': "❌ Error: Student ID '{id}' already exists!",
        'invalid_email': "❌ Error: Invalid email format!",
        'invalid_age': "❌ Error: Age must be between {min} and {max}!",
        'student_not_found': "❌ Student with ID '{id}' not found!",
        'file_not_found': "❌ File '{file}' not found!",
        'empty_field': "❌ {field} cannot be empty!",
        'invalid_choice': "❌ Invalid choice! Please enter a valid option.",
    }
    
    # Success messages
    SUCCESS_MESSAGES = {
        'student_added': "✅ Student '{name}' added successfully!",
        'student_updated': "✅ Student '{name}' updated successfully!",
        'student_deleted': "✅ Student '{name}' deleted successfully!",
        'data_saved': "✅ Data saved successfully!",
        'data_loaded': "✅ Loaded {count} student records!",
    }
    
    # Menu options
    MAIN_MENU = {
        '1': 'Add New Student',
        '2': 'View All Students',
        '3': 'Search Student',
        '4': 'Update Student',
        '5': 'Delete Student',
        '6': 'Sort Students',
        '7': 'Export Data',
        '8': 'Import Data',
        '9': 'Change File Format',
        '0': 'Exit'
    }
    
    # Sort options
    SORT_OPTIONS = {
        '1': 'name',
        '2': 'age',
        '3': 'grade'
    }
    
    # Export/Import formats
    FORMAT_OPTIONS = {
        '1': 'json',
        '2': 'csv'
    }
    
    @classmethod
    def get_data_file_path(cls, format_type: str = 'json') -> str:
        """Get the data file path based on format"""
        if format_type.lower() == 'json':
            return cls.DEFAULT_JSON_FILE
        elif format_type.lower() == 'csv':
            return cls.DEFAULT_CSV_FILE
        else:
            return cls.DEFAULT_JSON_FILE
    
    @classmethod
    def get_demo_file_path(cls, format_type: str = 'json') -> str:
        """Get the demo file path based on format"""
        if format_type.lower() == 'json':
            return cls.DEMO_JSON_FILE
        elif format_type.lower() == 'csv':
            return cls.DEMO_CSV_FILE
        else:
            return cls.DEMO_JSON_FILE
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        try:
            # Check if required fields are defined
            assert cls.REQUIRED_FIELDS, "Required fields not defined"
            assert cls.MIN_AGE < cls.MAX_AGE, "Invalid age range"
            assert cls.SUPPORTED_FORMATS, "No supported formats defined"
            return True
        except AssertionError as e:
            print(f"❌ Configuration error: {e}")
            return False

# Create a global config instance
config = Config()

# Validate configuration on import
if not config.validate_config():
    print("⚠️ Warning: Configuration validation failed!")
