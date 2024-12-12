import re
import csv
import json
import threading

# 1. My Custom Library
class MyLibrary:
    @staticmethod
    def extract_emails(text):
        """Extracts all email addresses from a given string using regex."""
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        return re.findall(email_pattern, text)

    @staticmethod
    def validate_phone_number(phone_number):
        """Validates phone numbers in the format (xxx) xxx-xxxx or xxx-xxx-xxxx."""
        phone_pattern = r'^((\(\d{3}\)\s?)|(\d{3}-))?\d{3}-\d{4}$'
        return bool(re.match(phone_pattern, phone_number))

# 2. Object-Oriented Programming with Inheritance
class FileProcessor:
    """Base class to handle file reading and writing."""

    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        """Reads content from a file."""
        try:
            with open(self.filename, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            return []

    def write_file(self, content):
        """Writes content to a file."""
        with open(self.filename, 'w') as file:
            file.writelines(content)

class CSVProcessor(FileProcessor):
    """Gets class specifically for CSV files."""

    def read_csv(self):
        """Reads lines from a CSV file."""
        try:
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                return [row for row in reader]
        except FileNotFoundError:
            return []

    def write_csv(self, rows):
        """Writes lines to a CSV file."""
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

class JSONProcessor(FileProcessor):
    """Gets class specifically for JSON files."""

    def read_json(self):
        """Reads a JSON file and returns the data."""
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def write_json(self, data):
        """Writes data to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

# 3. File I/O
class ContactManager:
    """ Here I'm managing contacts and demonstrating regex and file I/O."""

    def __init__(self, csv_file, json_file):
        self.csv_processor = CSVProcessor(csv_file)
        self.json_processor = JSONProcessor(json_file)
        self.contacts = self.csv_processor.read_csv()
        self.metadata = self.json_processor.read_json()

    def add_contact(self, name, email, phone):
        """Adds a contact after validating email and phone number."""
        if not MyLibrary.extract_emails(email):
            raise ValueError("Invalid email format.")
        if not MyLibrary.validate_phone_number(phone):
            raise ValueError("Invalid phone number format.")
        self.contacts.append([name, email, phone])

    def save_contacts(self):
        """Saves all contacts to the file."""
        self.csv_processor.write_csv(self.contacts)

    def save_metadata(self, key, value):
        """Updates and saves metadata to the JSON file."""
        self.metadata[key] = value
        self.json_processor.write_json(self.metadata)

# 4. Testing 
import unittest

class TestMyLibrary(unittest.TestCase):
    def test_extract_emails(self):
        text = "Contact me at mol7@kent.ac.uk "
        self.assertEqual(MyLibrary.extract_emails(text), ['mol7@kent.ac.uk'])

    def test_validate_phone_number(self):
        self.assertTrue(MyLibrary.validate_phone_number("(123) 456-7890"))
        self.assertTrue(MyLibrary.validate_phone_number("123-456-7890"))
        self.assertFalse(MyLibrary.validate_phone_number("1234567890"))

class TestContactManager(unittest.TestCase):
    def setUp(self):
        self.manager = ContactManager('test_contacts.csv', 'test_metadata.json')

    def test_add_contact(self):
        self.manager.add_contact("Mol7", "Mol7@kent.ac.uk", "123-456-7890")
        self.assertEqual(self.manager.contacts[-1], ["Mol7", "Mol7@kent.ac.uk", "123-456-7890"])

    def test_add_invalid_email(self):
        with self.assertRaises(ValueError):
            self.manager.add_contact("Invalid Email", "invalid-email", "123-456-7890")

    def test_add_invalid_phone(self):
        with self.assertRaises(ValueError):
            self.manager.add_contact("Invalid Phone", "valid@example.com", "1234567890")

    def test_save_metadata(self):
        self.manager.save_metadata("last_updated", "11-12-2024")
        self.assertEqual(self.manager.metadata["last_updated"], "11-12-2024")

# 5. Example Usage
def background_task(manager):
    """Simulates a background task saving metadata."""
    manager.save_metadata("task_status", "running")
    print("Background task status saved.")

if __name__ == "__main__":
    # Unit Tests
    unittest.main(exit=False)

    # Example Run
    cm = ContactManager('contacts.csv', 'metadata.json')
    cm.add_contact("Mol7", "Mol7@kent.ac.uk", "(123) 456-7890")
    cm.save_contacts()
    cm.save_metadata("last_updated", "11-12-2024")

    # Run a background task
    thread = threading.Thread(target=background_task, args=(cm,))
    thread.start()
    thread.join()

    print("Contacts and metadata saved!")
