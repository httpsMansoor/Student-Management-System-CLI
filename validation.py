"""
Validation functions for the Student Management System
"""
import re

def validate_input(column_name, user_input, expected_type):
    """
    Validate user input based on column name and expected type.
    Returns (is_valid, value, error_message)
    """
    # Skip empty inputs
    if not user_input:
        return False, None, f"{column_name} cannot be empty. Please try again."

    # Validate the input based on the expected type
    try:
        if expected_type == 'int':
            if not user_input.isdigit():
                return False, None, f"Invalid input for {column_name}. Expected a positive integer. Please try again."
            value = int(user_input)
            
            # Additional validation for age
            if column_name.lower() == 'age':
                if value < 5 or value > 100:
                    return False, None, "Age must be between 5 and 100 years. Please try again."
            
            # Additional validation for roll number
            elif column_name.lower() == 'roll number':
                if value < 1:
                    return False, None, "Roll Number must be a positive number. Please try again."
                if len(str(value)) > 10:
                    return False, None, "Roll Number cannot be more than 10 digits. Please try again."
            
            # Additional validation for grades as int
            elif column_name.lower() == 'grades':
                if value < 0 or value > 100:
                    return False, None, "Grades must be between 0 and 100. Please try again."
            
            return True, value, None
        
        elif expected_type == 'float':
            try:
                value = float(user_input)
                if value < 0:
                    return False, None, f"Invalid input for {column_name}. Expected a positive number. Please try again."
                return True, value, None
            except ValueError:
                return False, None, f"Invalid input for {column_name}. Expected a valid number. Please try again."
        
        elif expected_type == 'str':
            # Additional validation for specific fields
            if column_name.lower() == 'name':
                if not all(c.isalpha() or c.isspace() for c in user_input):
                    return False, None, "Name should only contain letters and spaces. Please try again."
                if len(user_input) < 2:
                    return False, None, "Name must be at least 2 characters long. Please try again."
            
            elif column_name.lower() == 'email':
                # Check minimum length
                if len(user_input) < 5:
                    return False, None, "Email must be at least 5 characters long. Please try again."
                
                # Check for @ symbol
                if '@' not in user_input:
                    return False, None, "Email must contain '@' symbol. Please try again."
                
                # Basic email regex pattern
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, user_input):
                    return False, None, "Invalid email format. Please enter a valid email address."
                
                try:
                    # Split email into username and domain
                    username, domain = user_input.split('@', 1)
                    
                    # Validate username
                    if len(username) < 1:
                        return False, None, "Email username cannot be empty. Please try again."
                    
                    if len(username) > 64:
                        return False, None, "Email username is too long. Maximum length is 64 characters."
                    
                    # Validate domain
                    valid_domains = [
                        'gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com', 
                        'icloud.com', 'protonmail.com', 'aol.com', 'mail.com',
                        'zoho.com', 'yandex.com', 'gmx.com', 'live.com'
                    ]
                    
                    # Check if domain ends with any valid domain
                    valid_domain_found = False
                    for valid_domain in valid_domains:
                        if domain.lower() == valid_domain:
                            valid_domain_found = True
                            break
                    
                    if not valid_domain_found:
                        return False, None, f"Invalid email domain. Please use one of these domains: {', '.join(valid_domains)}"
                    
                    # Check for special characters in username
                    if not re.match(r'^[a-zA-Z0-9._%+-]+$', username):
                        return False, None, "Email username can only contain letters, numbers, and these special characters: . _ % + -"
                    
                    # Check total length
                    if len(user_input) > 254:  # RFC 5321 standard
                        return False, None, "Email is too long. Maximum length is 254 characters."
                
                except ValueError:
                    return False, None, "Invalid email format. Please try again."
            
            elif column_name.lower() == 'phone':
                if not user_input.isdigit():
                    return False, None, "Phone number must contain only digits. Please try again."
                if len(user_input) < 10:
                    return False, None, "Phone number must be at least 10 digits long. Please try again."
                if len(user_input) > 15:
                    return False, None, "Phone number cannot be more than 15 digits. Please try again."
            
            elif column_name.lower() == 'address':
                if len(user_input) < 10:
                    return False, None, "Address must be at least 10 characters long. Please provide a complete address."
                # Check if address contains at least one number and one letter
                if not any(c.isdigit() for c in user_input):
                    return False, None, "Address must contain at least one number. Please try again."
                if not any(c.isalpha() for c in user_input):
                    return False, None, "Address must contain at least one letter. Please try again."
            
            elif column_name.lower() == 'class':
                if not user_input.isalnum():
                    return False, None, "Class should contain only letters and numbers. Please try again."
                if len(user_input) < 2:
                    return False, None, "Class must be at least 2 characters long. Please try again."
                if len(user_input) > 10:
                    return False, None, "Class name cannot be more than 10 characters. Please try again."
            
            return True, str(user_input), None
        
        else:
            return False, None, f"Unsupported type {expected_type} for column {column_name}. Please try again."
    
    except ValueError:
        return False, None, f"Invalid input for {column_name}. Expected {expected_type}. Please try again."

def get_valid_input(column_name, expected_type):
    """Helper function to get valid input from the user based on the expected type."""
    while True:
        user_input = input(f"Enter {column_name}: ").strip()
        is_valid, value, error_message = validate_input(column_name, user_input, expected_type)
        
        if is_valid:
            return value
        else:
            print(error_message) 