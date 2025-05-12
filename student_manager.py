"""
Student Manager for the Student Management System
"""
import os
import csv
import json
from student import Student
from validation import get_valid_input
from utils import ensure_directory_exists, normalize_file_path

class StudentManager:
    def __init__(self, file_path='students.csv'):
        # Only use filename without path by default, so it works in current directory
        if os.path.dirname(file_path) == '':
            self.file_path = file_path  # Just use the filename in current directory
        else:
            self.file_path = file_path  # Use provided path
        self.students = []
        self.columns = []  # Start with an empty columns list
        self.column_types = {}  # To store expected types for each column
        self._load_data()

    def _load_data(self):
        """Load existing data from CSV if available."""
        if not os.path.exists(self.file_path):
            print(f"Error: The file '{self.file_path}' does not exist.")
            return

        try:
            with open(self.file_path, mode="r") as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Get the header row
                if header and len(header) > 1:
                    self.columns = json.loads(header[1])  # Deserialize JSON column names (stored in first row)
                    
                    # Define default column types
                    default_column_types = {
                        'Name': 'str',
                        'Age': 'int',
                        'Email': 'str',
                        'Phone': 'str',
                        'Address': 'str',
                        'Class': 'str',
                        'Roll Number': 'int',
                        'Grades': 'str'
                    }
                    
                    # Initialize column types
                    self.column_types = default_column_types
                    
                    # Fix any RollNo to Roll Number in columns
                    if 'RollNo' in self.columns and 'Roll Number' not in self.columns:
                        self.columns = [col if col != 'RollNo' else 'Roll Number' for col in self.columns]
                else:
                    print(f"Error: The file '{self.file_path}' does not have valid column data.")
                    return

                for row in csv_reader:
                    if row:
                        student_id, student_json = row
                        try:
                            student_data = json.loads(student_json)  # Deserialize JSON data
                            
                            # Fix RollNo to Roll Number in student data
                            if 'RollNo' in student_data and 'Roll Number' not in student_data:
                                student_data['Roll Number'] = student_data.pop('RollNo')
                            
                            student_data.pop('ID', None)  # Remove 'ID' from student_data and pass separately to avoid conflict
                            self.students.append(Student(ID=student_id, **student_data))  # Pass student_id separately
                        except json.JSONDecodeError:
                            print(f"Error: Invalid JSON format in row for student ID {student_id}.")
                            continue
        except (OSError, IOError) as e:
            print(f"Error: Could not open or read the file '{self.file_path}'. Error: {e}")
        except Exception as e:
            print(f"Unexpected error while loading data: {e}")

    def _save_data(self):
        """Save data into the CSV file as JSON."""
        try:
            # Create directory if it doesn't exist (for new paths with directories)
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(self.file_path, mode="w", newline="") as file:
                csv_writer = csv.writer(file)
                # Save the columns in the first row as JSON
                csv_writer.writerow(["Columns", json.dumps(self.columns)])  # Save the column names as JSON
                for student in self.students:
                    student_json = student.to_json()  # Serialize student data to JSON
                    csv_writer.writerow([student.data['ID'], student_json])  # Write student data
        except (OSError, IOError) as e:
            print(f"Error: Could not write to the file '{self.file_path}'. Error: {e}")
        except Exception as e:
            print(f"Unexpected error while saving data: {e}")

    def _check_unique_id(self, student_id):
        """Check if the student ID is unique."""
        return all(student.data['ID'] != student_id for student in self.students)

    def _check_unique_roll_number(self, roll_number):
        """Check if the roll number is unique."""
        try:
            return all(student.data.get('Roll Number') != roll_number for student in self.students)
        except Exception:
            return True  # If there's any error, assume the roll number is unique

    def add_student(self):
        """Add a new student."""
        # Ensure file exists, create if not
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' does not exist. Creating a new file...")
            try:
                self._setup_new_file()
            except Exception as e:
                print(f"Error: Failed to create and save the new file. Error: {e}")
                return

        # Now, ask for the student data and add it to the file
        student_data = {}

        # Check for unique ID with validation
        while True:
            student_id = input("Enter student ID (numbers only): ").strip()
            if not student_id.isdigit():
                print("Student ID must contain only numbers. Please try again.")
                continue
            if not self._check_unique_id(student_id):
                print(f"Error: Student with ID {student_id} already exists. Please enter a unique ID.")
            else:
                student_data['ID'] = student_id
                break

        print("\nEnter the student data:")
        # Ask for data based on expected types for each column
        for column in self.columns:
            if column != 'ID':  # Skip ID as it's already handled
                expected_type = self.column_types.get(column, 'str')  # Default to 'str' if no type defined
                if column == 'Roll Number':
                    # Special handling for Roll Number to check uniqueness
                    while True:
                        roll_number = get_valid_input(column, expected_type)
                        if not self._check_unique_roll_number(roll_number):
                            print(f"Error: Student with roll number {roll_number} already exists. Please enter a unique roll number.")
                            continue
                        student_data[column] = roll_number
                        break
                else:
                    student_data[column] = get_valid_input(column, expected_type)

        student = Student(**student_data)
        self.students.append(student)
        self._save_data()
        print("Student added successfully!")

    def view_students(self):
        """View all students in a human-readable format."""
        if not self.students:
            print(f"No student data found in file: {self.file_path}")
        else:
            print(f"Student Data from file: {self.file_path}")
            print(f"Total students: {len(self.students)}")
            print("-" * 40)
            for student in self.students:
                print(student.display())
                print("-" * 40)  # A separator for each student

    def update_student(self):
        """Update an existing student."""
        # Ensure file exists before updating
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' does not exist. Please create it first.")
            return
        
        student_id = input("Enter student ID to update: ")
        student = next((s for s in self.students if s.data.get("ID") == student_id), None)
        if student:
            for key, value in student.to_dict().items():
                if key != 'ID':  # Don't allow ID to be updated
                    expected_type = self.column_types.get(key, 'str')
                    if key == 'Roll Number':
                        # Special handling for Roll Number to check uniqueness
                        while True:
                            new_value = get_valid_input(f"new {key}", expected_type)
                            if new_value != value and not self._check_unique_roll_number(new_value):
                                print(f"Error: Student with roll number {new_value} already exists. Please enter a unique roll number.")
                                continue
                            student.data[key] = new_value
                            break
                    else:
                        new_value = get_valid_input(f"new {key}", expected_type)
                        student.data[key] = new_value
            self._save_data()
            print("Student information updated successfully!")
        else:
            print(f"No student found with ID {student_id}")

    def delete_student(self):
        """Delete a student."""
        # Ensure file exists before deleting
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' does not exist. Please create it first.")
            return
        
        student_id = input("Enter student ID to delete: ")
        student = next((s for s in self.students if s.data.get("ID") == student_id), None)
        if student:
            self.students.remove(student)
            self._save_data()
            print(f"Student with ID {student_id} deleted.")
        else:
            print(f"No student found with ID {student_id}")

    def add_column(self):
        """Add a new column to the data."""
        # Ensure file exists before adding a column
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' does not exist. Please create it first.")
            return
        
        new_column = input("Enter new column name: ")
        if not new_column.strip():
            print("Column name cannot be empty. Operation canceled.")
            return
            
        if new_column in self.columns:
            print(f"Column '{new_column}' already exists. Please use a different name.")
            return
            
        # Ask for column position
        print("\nWhere would you like to add the new column?")
        print("1. At the beginning")
        print("2. At the end")
        print("3. At a specific position")
        
        while True:
            position_choice = input("Enter your choice (1-3): ")
            
            if position_choice == '1':
                # Add at the beginning
                self.columns.insert(0, new_column)
                break
            elif position_choice == '2':
                # Add at the end
                self.columns.append(new_column)
                break
            elif position_choice == '3':
                # Add at a specific position
                if len(self.columns) > 0:
                    print("\nCurrent columns:")
                    for i, col in enumerate(self.columns):
                        print(f"{i+1}. {col}")
                        
                    while True:
                        try:
                            pos = int(input(f"Enter position (1-{len(self.columns)+1}): "))
                            if 1 <= pos <= len(self.columns) + 1:
                                self.columns.insert(pos - 1, new_column)
                                break
                            else:
                                print(f"Please enter a number between 1 and {len(self.columns)+1}.")
                        except ValueError:
                            print("Please enter a valid number.")
                else:
                    # If no columns, just add it
                    self.columns.append(new_column)
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                
        # Ask for column type
        new_column_type = input(f"Enter the expected type for new column {new_column} (str, int, float): ")
        if new_column_type.strip().lower() not in ['str', 'int', 'float']:
            print(f"Invalid type '{new_column_type}'. Using 'str' as default.")
            new_column_type = 'str'
        
        self.column_types[new_column] = new_column_type.strip().lower()
        
        # Add the column to all existing student records
        for student in self.students:
            student.data[new_column] = get_valid_input(new_column, self.column_types[new_column])
            
        self._save_data()
        print(f"Column '{new_column}' added successfully at position {self.columns.index(new_column) + 1}.")

    def delete_column(self):
        """Delete a column from the data."""
        # Ensure file exists before deleting a column
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' does not exist. Please create it first.")
            return
            
        if not self.columns:
            print("No columns available to delete.")
            return
            
        # Show available columns
        print("Available columns:")
        for i, column in enumerate(self.columns, 1):
            print(f"{i}. {column}")
            
        # Protected columns that cannot be deleted
        protected_columns = ['Roll Number', 'ID']
            
        while True:
            try:
                column_choice = input("\nEnter the number of the column to delete (0 to cancel): ")
                
                if column_choice == '0':
                    print("Column deletion cancelled.")
                    return
                    
                column_index = int(column_choice) - 1
                
                if 0 <= column_index < len(self.columns):
                    column_to_delete = self.columns[column_index]
                    
                    if column_to_delete in protected_columns:
                        print(f"Error: Cannot delete the '{column_to_delete}' column as it's required for student identification.")
                        continue
                        
                    # Confirm deletion
                    confirm = input(f"Are you sure you want to delete the '{column_to_delete}' column? (y/n): ")
                    
                    if confirm.lower() != 'y':
                        print("Column deletion cancelled.")
                        return
                        
                    # Remove column from data structure
                    self.columns.remove(column_to_delete)
                    if column_to_delete in self.column_types:
                        self.column_types.pop(column_to_delete)
                        
                    # Remove column from all student records
                    for student in self.students:
                        if column_to_delete in student.data:
                            student.data.pop(column_to_delete)
                            
                    self._save_data()
                    print(f"Column '{column_to_delete}' deleted successfully.")
                    return
                else:
                    print("Invalid column number. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def replace_column(self):
        """Replace or rename a column in the data."""
        # Ensure file exists before replacing a column
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' does not exist. Please create it first.")
            return
            
        if not self.columns:
            print("No columns available to replace.")
            return
            
        # Show available columns
        print("Available columns:")
        for i, column in enumerate(self.columns, 1):
            print(f"{i}. {column}")
            
        # Protected columns that cannot be replaced
        protected_columns = ['ID']
            
        while True:
            try:
                column_choice = input("\nEnter the number of the column to replace (0 to cancel): ")
                
                if column_choice == '0':
                    print("Column replacement cancelled.")
                    return
                    
                column_index = int(column_choice) - 1
                
                if 0 <= column_index < len(self.columns):
                    column_to_replace = self.columns[column_index]
                    
                    if column_to_replace in protected_columns:
                        print(f"Error: Cannot replace the '{column_to_replace}' column as it's a system column.")
                        continue
                        
                    # Get new column name
                    new_column_name = input(f"Enter new name for column '{column_to_replace}': ")
                    
                    if not new_column_name.strip():
                        print("Column name cannot be empty. Operation canceled.")
                        return
                        
                    if new_column_name in self.columns:
                        print(f"Column '{new_column_name}' already exists. Please use a different name.")
                        continue
                        
                    # Ask if they want to change the data type
                    current_type = self.column_types.get(column_to_replace, 'str')
                    change_type = input(f"Current data type is '{current_type}'. Do you want to change it? (y/n): ")
                    
                    if change_type.lower() == 'y':
                        while True:
                            new_type = input(f"Enter new data type for column '{new_column_name}' (str, int, float): ")
                            if new_type.lower() in ['str', 'int', 'float']:
                                break
                            else:
                                print("Invalid type. Please use 'str', 'int', or 'float'.")
                    else:
                        new_type = current_type
                        
                    # Confirm replacement
                    confirm = input(f"Are you sure you want to replace '{column_to_replace}' with '{new_column_name}'? (y/n): ")
                    
                    if confirm.lower() != 'y':
                        print("Column replacement cancelled.")
                        return
                        
                    # Perform the replacement
                    # Update column name in the list
                    self.columns[column_index] = new_column_name
                    
                    # Update column type
                    if column_to_replace in self.column_types:
                        self.column_types[new_column_name] = new_type
                        del self.column_types[column_to_replace]
                    else:
                        self.column_types[new_column_name] = new_type
                        
                    # Update all student records
                    for student in self.students:
                        if column_to_replace in student.data:
                            # First convert value to the proper type if needed
                            old_value = student.data[column_to_replace]
                            
                            if current_type != new_type:
                                # If changing type, ask for a new value
                                print(f"\nCurrent value '{old_value}' needs to be converted to {new_type} for student ID {student.data.get('ID', 'unknown')}.")
                                student.data[new_column_name] = get_valid_input(new_column_name, new_type)
                            else:
                                # If same type, just move the value
                                student.data[new_column_name] = old_value
                                
                            # Remove the old column
                            del student.data[column_to_replace]
                    
                    self._save_data()
                    print(f"Column '{column_to_replace}' replaced with '{new_column_name}' successfully.")
                    return
                else:
                    print("Invalid column number. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def change_file_path(self):
        """Allow the user to change the file path."""
        print("\nChange File Path Options:")
        print("1. Create new file in current directory")
        print("2. Browse existing CSV files in current directory")
        print("3. Enter an absolute path")
        print("4. Cancel")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            # Create new file in current directory
            print("\nCreate a new file in the current directory:")
            new_file_path = input("Enter new file name (without extension): ")
            if not new_file_path.strip():
                print("File name cannot be empty. Operation canceled.")
                return
                
            # Make sure path has .csv extension
            new_file_path = normalize_file_path(new_file_path)
                
            # Check if file already exists
            if os.path.exists(new_file_path):
                overwrite = input(f"File '{new_file_path}' already exists. Overwrite? (y/n): ")
                if overwrite.lower() != 'y':
                    print("Operation canceled.")
                    return
                print(f"Existing file '{new_file_path}' will be overwritten.")
            else:
                print(f"New file '{new_file_path}' will be created in the current directory.")
                
            # Confirm creation
            confirm = input("Confirm file creation? (y/n): ")
            if confirm.lower() != 'y':
                print("Operation canceled.")
                return
        
        elif choice == '2':
            # Browse existing CSV files
            from utils import get_csv_files_in_directory
            print("\nAvailable CSV files in current directory:")
            csv_files = get_csv_files_in_directory()
            
            if not csv_files:
                print("No CSV files found in current directory.")
                return
                
            for i, file in enumerate(csv_files, 1):
                print(f"{i}. {file}")
                
            while True:
                try:
                    file_choice = input("\nSelect a file (0 to cancel): ")
                    if file_choice == '0':
                        print("Operation canceled.")
                        return
                        
                    file_index = int(file_choice) - 1
                    if 0 <= file_index < len(csv_files):
                        new_file_path = csv_files[file_index]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(csv_files)}.")
                except ValueError:
                    print("Please enter a valid number.")
        
        elif choice == '3':
            # Absolute path
            new_file_path = input("Enter absolute file path (e.g., C:\\path\\to\\file.csv): ")
            if not new_file_path.strip():
                print("File path cannot be empty. Operation canceled.")
                return
                
            # Make sure path has .csv extension
            new_file_path = normalize_file_path(new_file_path)
                
            # Verify if directory exists
            if not ensure_directory_exists(new_file_path):
                return
        
        elif choice == '4':
            print("Operation canceled.")
            return
            
        else:
            print("Invalid choice. Operation canceled.")
            return
        
        # At this point we have a valid new_file_path
        print(f"\nChanging file path from '{self.file_path}' to '{new_file_path}'")
        
        # Save current data to old path before changing
        self._save_data()
        
        # Store old file path in case we need to revert
        old_file_path = self.file_path
        
        # Update the file path
        self.file_path = new_file_path
        
        # Clear current data
        self.students = []
        
        # Check if new file exists
        if os.path.exists(self.file_path):
            print(f"Loading data from existing file: {self.file_path}")
            try:
                self._load_data()
                print(f"Successfully loaded {len(self.students)} student records.")
            except Exception as e:
                print(f"Error loading data from new file: {e}")
                # Revert to old file path if loading fails
                print(f"Reverting back to previous file: {old_file_path}")
                self.file_path = old_file_path
                self._load_data()
                return
        else:
            print(f"File '{self.file_path}' does not exist. Creating a new file...")
            # Reset columns to empty before creating new file
            self.columns = []
            self.column_types = {}
            
            # Prompt user to set up columns for the new file
            self._setup_new_file()
        
        print(f"File path changed to: {self.file_path}")
        # Ask if user wants to make this file the default for future program runs
        default_choice = input("Would you like to make this the default file for future runs? (y/n): ")
        if default_choice.lower() == 'y':
            from utils import save_config
            config = {'default_file_path': self.file_path}
            if save_config(config):
                print(f"Default file set to: {self.file_path}")

    def _setup_new_file(self):
        """Set up columns for a new file."""
        # Define default columns with their types
        default_columns = {
            'Name': 'str',
            'Roll Number': 'int',
            'Age': 'int',
            'Email': 'str',
            'Phone': 'str',
            'Address': 'str',
            'Class': 'str',
            'Grades': 'str'
        }
        
        print("Choose column setup:")
        print("1. Use default columns (Name, Roll Number, Age, Email, Phone, Address, Class, Grades)")
        print("2. Define custom columns")
        
        while True:
            choice = input("Enter your choice (1 or 2): ")
            if choice == '1':
                print("\nCreating new file with default columns:")
                for col, col_type in default_columns.items():
                    print(f"- {col} ({col_type})")
                
                self.columns = list(default_columns.keys())
                self.column_types = default_columns
                break
            elif choice == '2':
                custom_columns = {}
                print("\nDefine your custom columns:")
                print("Enter column names and types. Type 'done' when finished.")
                print("Available types: str, int, float")
                
                while True:
                    col_name = input("Enter column name (or 'done' to finish): ")
                    if col_name.lower() == 'done':
                        break
                    
                    if not col_name.strip():
                        print("Column name cannot be empty. Please try again.")
                        continue
                        
                    while True:
                        col_type = input(f"Enter type for '{col_name}' (str, int, float): ").lower()
                        if col_type in ['str', 'int', 'float']:
                            custom_columns[col_name] = col_type
                            break
                        else:
                            print("Invalid type. Please use 'str', 'int', or 'float'.")
                
                if not custom_columns:
                    print("No columns defined. Using default columns.")
                    self.columns = list(default_columns.keys())
                    self.column_types = default_columns
                else:
                    # Add Roll Number if not already added to ensure uniqueness
                    if 'Roll Number' not in custom_columns:
                        print("Note: 'Roll Number' column added automatically (required for student identification)")
                        custom_columns['Roll Number'] = 'int'
                    
                    print("\nCreating new file with custom columns:")
                    for col, col_type in custom_columns.items():
                        print(f"- {col} ({col_type})")
                    
                    self.columns = list(custom_columns.keys())
                    self.column_types = custom_columns
                break
            else:
                print("Invalid choice! Please enter 1 or 2.")
        
        print(f"\nNew file created with columns: {self.columns}")
        # Save the file with the columns
        self._save_data()

    def show_menu(self):
        """Display the menu options."""
        print("\n1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Add Column")
        print("6. Delete Column")
        print("7. Replace Column")
        print("8. Change File Path")
        print("9. Exit")
        
    def run(self):
        """Run the CLI interface."""
        while True:
            self.show_menu()
            try:
                choice = input("Enter your choice: ")
                if choice == '1':
                    self.add_student()
                elif choice == '2':
                    self.view_students()
                elif choice == '3':
                    self.update_student()
                elif choice == '4':
                    self.delete_student()
                elif choice == '5':
                    self.add_column()
                elif choice == '6':
                    self.delete_column()
                elif choice == '7':
                    self.replace_column()
                elif choice == '8':
                    self.change_file_path()
                elif choice == '9':
                    print("Exiting program.")
                    break
                else:
                    print("Invalid choice! Please try again.")
            except EOFError:
                print("\nEOFError: No input received. Exiting...")
                break 