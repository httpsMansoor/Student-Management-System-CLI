"""
Student Management System - Main Entry Point
"""
import os
from student_manager import StudentManager
from utils import load_config, save_config

def main():
    # Print header
    print("="*50)
    print("       STUDENT MANAGEMENT SYSTEM")
    print("="*50)
    
    # Load configuration
    config = load_config()
    default_file_path = config.get('default_file_path', 'students.csv')
    
    # Check if file exists
    if not os.path.exists(default_file_path):
        print(f"Default file '{default_file_path}' not found.")
        create_new = input("Would you like to create a new file? (y/n): ")
        if create_new.lower() != 'y':
            print("Using default students.csv in root directory instead.")
            default_file_path = 'students.csv'
            # Update the config to use this file for next time
            config = {'default_file_path': default_file_path}
            save_config(config)
    
    print(f"Using data file: {default_file_path}")
    
    # Initialize and run the student manager
    student_manager = StudentManager(default_file_path)
    student_manager.run()

if __name__ == "__main__":
    main() 