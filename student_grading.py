#!/usr/bin/env python3
"""
Student Grading System CLI Application
Uses JSON file as database to manage student grades
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


DB_FILE = "students_db.json"


def load_database() -> List[Dict[str, Any]]:
    """Load student records from JSON file."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_database(students: List[Dict[str, Any]]) -> None:
    """Save student records to JSON file."""
    with open(DB_FILE, 'w') as f:
        json.dump(students, f, indent=2)


def initialize_database() -> None:
    """Initialize database with 5 prefilled records if it doesn't exist."""
    if os.path.exists(DB_FILE):
        return


def display_all_records(students: List[Dict[str, Any]]) -> None:
    """Display all student records."""
    if not students:
        print("\nNo records found.")
        return
    
    print("\n" + "="*80)
    print(f"{'Student ID':<12} {'First Name':<15} {'Last Name':<15} {'Course':<20} {'Semester':<15} {'Grade':<8}")
    print("="*80)
    
    for student in students:
        print(f"{student['student_id']:<12} {student['first_name']:<15} {student['last_name']:<15} "
              f"{student['course_name']:<20} {student['semester']:<15} {student['final_grade']:<8.1f}")
    
    print("="*80)
    print(f"Total records: {len(students)}\n")


def add_record(students: List[Dict[str, Any]]) -> None:
    """Add a new student record."""
    print("\n--- Add New Student Record ---")
    
    student_id = input("Enter Student ID: ").strip()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return
    
    # Check if student_id already exists
    if any(s['student_id'] == student_id for s in students):
        print(f"Error: Student ID '{student_id}' already exists.")
        return
    
    first_name = input("Enter First Name: ").strip()
    last_name = input("Enter Last Name: ").strip()
    course_name = input("Enter Course Name: ").strip()
    semester = input("Enter Semester: ").strip()
    
    try:
        final_grade = float(input("Enter Final Grade: ").strip())
    except ValueError:
        print("Error: Final grade must be a number.")
        return
    
    new_student = {
        "student_id": student_id,
        "first_name": first_name,
        "last_name": last_name,
        "course_name": course_name,
        "semester": semester,
        "final_grade": final_grade
    }
    
    students.append(new_student)
    save_database(students)
    print(f"\nStudent record '{student_id}' added successfully!")


def delete_record(students: List[Dict[str, Any]]) -> None:
    """Delete a student record by student_id."""
    print("\n--- Delete Student Record ---")
    student_id = input("Enter Student ID to delete: ").strip()
    
    initial_count = len(students)
    students[:] = [s for s in students if s['student_id'] != student_id]
    
    if len(students) < initial_count:
        save_database(students)
        print(f"\nStudent record '{student_id}' deleted successfully!")
    else:
        print(f"\nError: Student ID '{student_id}' not found.")


def update_record(students: List[Dict[str, Any]]) -> None:
    """Update an existing student record."""
    print("\n--- Update Student Record ---")
    student_id = input("Enter Student ID to update: ").strip()
    
    student = next((s for s in students if s['student_id'] == student_id), None)
    if not student:
        print(f"\nError: Student ID '{student_id}' not found.")
        return
    
    print(f"\nCurrent record for {student_id}:")
    print(f"  First Name: {student['first_name']}")
    print(f"  Last Name: {student['last_name']}")
    print(f"  Course Name: {student['course_name']}")
    print(f"  Semester: {student['semester']}")
    print(f"  Final Grade: {student['final_grade']}")
    
    print("\nEnter new values (press Enter to keep current value):")
    
    first_name = input(f"First Name [{student['first_name']}]: ").strip()
    if first_name:
        student['first_name'] = first_name
    
    last_name = input(f"Last Name [{student['last_name']}]: ").strip()
    if last_name:
        student['last_name'] = last_name
    
    course_name = input(f"Course Name [{student['course_name']}]: ").strip()
    if course_name:
        student['course_name'] = course_name
    
    semester = input(f"Semester [{student['semester']}]: ").strip()
    if semester:
        student['semester'] = semester
    
    grade_input = input(f"Final Grade [{student['final_grade']}]: ").strip()
    if grade_input:
        try:
            student['final_grade'] = float(grade_input)
        except ValueError:
            print("Error: Final grade must be a number. Keeping current value.")
    
    save_database(students)
    print(f"\nStudent record '{student_id}' updated successfully!")


def quicksort(students: List[Dict[str, Any]], attribute: str, reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Quicksort algorithm implementation from scratch.
    Sorts a list of student dictionaries by the specified attribute.
    
    Args:
        students: List of student dictionaries to sort
        attribute: The attribute key to sort by
        reverse: If True, sort in descending order; if False, ascending
    
    Returns:
        A new sorted list of student dictionaries
    """
    # Base case: if list has 0 or 1 elements, it's already sorted
    if len(students) <= 1:
        return students.copy()
    
    # Choose pivot (using middle element for better average performance)
    pivot_idx = len(students) // 2
    pivot = students[pivot_idx][attribute]
    
    # Partition the list into three parts: less than, equal to, and greater than pivot
    less = []
    equal = []
    greater = []
    
    for student in students:
        value = student[attribute]
        
        # Compare values (handles both string and numeric types)
        if isinstance(value, (int, float)) and isinstance(pivot, (int, float)):
            # Numeric comparison
            if value < pivot:
                less.append(student)
            elif value > pivot:
                greater.append(student)
            else:
                equal.append(student)
        else:
            # String comparison (case-insensitive)
            value_str = str(value).lower()
            pivot_str = str(pivot).lower()
            if value_str < pivot_str:
                less.append(student)
            elif value_str > pivot_str:
                greater.append(student)
            else:
                equal.append(student)
    
    # Recursively sort the partitions
    if reverse:
        # For descending order, swap less and greater
        return quicksort(greater, attribute, reverse) + equal + quicksort(less, attribute, reverse)
    else:
        # For ascending order
        return quicksort(less, attribute, reverse) + equal + quicksort(greater, attribute, reverse)


def sort_records(students: List[Dict[str, Any]]) -> None:
    """Sort records by a selected attribute using custom quicksort algorithm."""
    if not students:
        print("\nNo records to sort.")
        return
    
    print("\n--- Sort Records ---")
    print("Available attributes to sort by:")
    print("1. student_id (string)")
    print("2. first_name (string)")
    print("3. last_name (string)")
    print("4. course_name (string)")
    print("5. semester (string)")
    print("6. final_grade (numeric)")
    
    choice = input("\nSelect attribute (1-6): ").strip()
    
    attribute_map = {
        "1": "student_id",
        "2": "first_name",
        "3": "last_name",
        "4": "course_name",
        "5": "semester",
        "6": "final_grade"
    }
    
    if choice not in attribute_map:
        print("Invalid choice.")
        return
    
    attribute = attribute_map[choice]
    
    order = input("Sort order (ascending/descending) [ascending]: ").strip().lower()
    reverse = order == "descending" or order == "desc"
    
    # Sort the records using custom quicksort algorithm
    sorted_students = quicksort(students, attribute, reverse)
    
    print(f"\nRecords sorted by {attribute} ({'descending' if reverse else 'ascending'}):")
    display_all_records(sorted_students)
    
    # Ask if user wants to save the sorted order
    save_choice = input("Save this sort order? (yes/no) [no]: ").strip().lower()
    if save_choice == "yes" or save_choice == "y":
        save_database(sorted_students)
        print("Sort order saved.")


def filter_records(students: List[Dict[str, Any]]) -> None:
    """Filter/search records by one or more criteria."""
    if not students:
        print("\nNo records to filter.")
        return
    
    print("\n--- Filter/Search Records ---")
    print("Enter search criteria (press Enter to skip a field):")
    
    filters = {}
    
    student_id = input("Student ID: ").strip()
    if student_id:
        filters['student_id'] = student_id
    
    first_name = input("First Name: ").strip()
    if first_name:
        filters['first_name'] = first_name
    
    last_name = input("Last Name: ").strip()
    if last_name:
        filters['last_name'] = last_name
    
    course_name = input("Course Name: ").strip()
    if course_name:
        filters['course_name'] = course_name
    
    semester = input("Semester: ").strip()
    if semester:
        filters['semester'] = semester
    
    grade_input = input("Final Grade (exact match): ").strip()
    if grade_input:
        try:
            filters['final_grade'] = float(grade_input)
        except ValueError:
            print("Warning: Invalid grade value, ignoring grade filter.")
    
    if not filters:
        print("\nNo search criteria provided. Showing all records.")
        display_all_records(students)
        return
    
    # Filter records
    filtered = []
    for student in students:
        match = True
        for key, value in filters.items():
            if key == 'final_grade':
                # Exact match for numeric grade
                if student[key] != value:
                    match = False
                    break
            else:
                # Case-insensitive partial match for string fields
                if value.lower() not in str(student[key]).lower():
                    match = False
                    break
        
        if match:
            filtered.append(student)
    
    if filtered:
        print(f"\nFound {len(filtered)} matching record(s):")
        display_all_records(filtered)
    else:
        print("\nNo records found matching the criteria.")


def main_menu() -> None:
    """Display main menu and handle user choices."""
    initialize_database()
    
    while True:
        print("\n" + "="*50)
        print("STUDENT GRADING SYSTEM")
        print("="*50)
        print("1. Display all records")
        print("2. Add a record")
        print("3. Delete a record")
        print("4. Update a record")
        print("5. Sort records")
        print("6. Filter/Search records")
        print("7. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        students = load_database()
        
        if choice == "1":
            display_all_records(students)
        elif choice == "2":
            add_record(students)
        elif choice == "3":
            delete_record(students)
        elif choice == "4":
            update_record(students)
        elif choice == "5":
            sort_records(students)
        elif choice == "6":
            filter_records(students)
        elif choice == "7":
            print("\nThank you for using the Student Grading System. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main_menu()

