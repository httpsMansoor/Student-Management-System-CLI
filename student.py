"""
Student class for the Student Management System
"""
import json

class Student:
    def __init__(self, **kwargs):
        self.data = kwargs

    def __repr__(self):
        return json.dumps(self.data)

    def to_dict(self):
        return self.data

    def to_json(self):
        """Convert the student data to JSON format."""
        return json.dumps(self.data)

    def display(self):
        """Convert the student data to a human-readable string format."""
        display_string = ""
        for key, value in self.data.items():
            display_string += f"{key}: {value}\n"
        return display_string.strip() 