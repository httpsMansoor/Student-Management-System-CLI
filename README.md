# Student Management System

A comprehensive command-line application for managing student records with robust validation, flexible data storage options, and improved user experience.

## Features

- **Student Data Management**: Add, view, update, and delete student records
- **Data Validation**: Strict data validation for all student fields (email, age, phone, etc.)
- **Column Management**: Add, delete, or rename columns in the data structure
- **File Management**: Create new data files or work with existing ones
- **Configuration**: Save default file paths for future sessions

## System Requirements

- Python 3.6 or higher

## Installation

1. Clone or download this repository to your local machine
2. Navigate to the project directory

## Usage

Run the program by executing:

```
python main.py
```

### Menu Options

The system provides the following options:

1. **Add Student**: Add a new student record with validation
2. **View Students**: Display all student records from the current file
3. **Update Student**: Modify an existing student's information
4. **Delete Student**: Remove a student from the records
5. **Add Column**: Add a new data column with custom type
6. **Delete Column**: Remove an existing data column
7. **Replace Column**: Rename or change the data type of a column
8. **Change File Path**: Work with a different data file
9. **Exit**: Quit the application

### Data Storage

- The application stores data in CSV files with JSON-encoded student information
- The first row contains column definitions
- Each subsequent row contains a student ID and JSON data

## Project Structure

- `main.py` - Entry point for the application
- `student.py` - Definition of the Student class
- `student_manager.py` - StudentManager class for data operations
- `validation.py` - Functions for data validation
- `utils.py` - Utility functions for file operations

## Data Validation

The system includes robust validation for various data types:

- **Email**: Checks for valid format, length, and supported domains
- **Phone Numbers**: Ensures proper length and digit-only values
- **Names**: Validates proper formatting with letters only
- **Roll Numbers**: Ensures uniqueness and proper format
- **Ages**: Validates within reasonable range (5-100)

## Customization

You can customize your student database by:
- Creating new CSV files with custom columns
- Adding or removing columns in existing files
- Changing column data types (string, integer, float)

## Default Configuration

The system will remember your last used file path by storing it in a `config.json` file. This allows you to pick up where you left off in future sessions. 