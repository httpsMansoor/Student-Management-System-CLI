"""
Utility functions for the Student Management System
"""
import os
import json

def ensure_directory_exists(filepath):
    """
    Ensure that the directory for the given filepath exists.
    Creates directories if they don't exist.
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully.")
            return True
        except Exception as e:
            print(f"Failed to create directory: {e}")
            return False
    return True

def get_csv_files_in_directory(directory='.'):
    """
    Get a list of all CSV files in the specified directory.
    """
    return [f for f in os.listdir(directory) if f.endswith('.csv')]

def normalize_file_path(file_path):
    """
    Normalize a file path to ensure it has a .csv extension and is valid.
    Returns the normalized path.
    """
    # Make sure path has .csv extension
    if not file_path.endswith('.csv'):
        file_path += '.csv'
    return file_path

def load_config():
    """
    Load the configuration file for default settings.
    """
    config = {'default_file_path': 'students.csv'}
    try:
        if os.path.exists('config.json'):
            with open('config.json', 'r') as config_file:
                loaded_config = json.load(config_file)
                config.update(loaded_config)
    except Exception as e:
        print(f"Error reading config file: {e}")
    return config

def save_config(config):
    """
    Save the configuration to a file.
    """
    try:
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
        return True
    except Exception as e:
        print(f"Failed to save config: {e}")
        return False 