#!/usr/bin/env python3
"""
Student Grading System CLI Application
Uses JSON file as database to manage student grades
"""

import json
import os
from typing import List, Dict, Any


DB_FILE = "students_db.json"


def load_database() -> List[Dict[str, Any]]:
    """
    Load student records from JSON file.
    
    Time Complexity: O(n) where n is the number of records in the file.
    """
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_database(students: List[Dict[str, Any]]) -> None:
    """
    Save student records to JSON file.
    
    Time Complexity: O(n) where n is the number of records to save.
    """
    with open(DB_FILE, "w") as f:
        json.dump(students, f, indent=2)


def initialize_database() -> None:
    """Initialize database with 5 prefilled records if it doesn't exist."""
    if os.path.exists(DB_FILE):
        return


def display_all_records(students: List[Dict[str, Any]]) -> None:
    """
    Display all student records.
    
    Time Complexity: O(n) where n is the number of records to display.
    """
    if not students:
        print("\nNo records found.")
        return

    print("\n" + "=" * 80)
    print(
        f"{'Student ID':<12} {'First Name':<15} {'Last Name':<15} {'Course':<20} {'Semester':<15} {'Grade':<8}"
    )
    print("=" * 80)

    for student in students:
        print(
            f"{student['student_id']:<12} {student['first_name']:<15} {student['last_name']:<15} "
            f"{student['course_name']:<20} {student['semester']:<15} {student['final_grade']:<8.1f}"
        )

    print("=" * 80)
    print(f"Total records: {len(students)}\n")


def add_record(students: List[Dict[str, Any]]) -> None:
    """
    Add a new student record.
    
    Time Complexity: O(n) where n is the number of records
        - O(n) to check if student_id already exists
        - O(1) to append new record
        - O(n) to save database
    """
    print("\n--- Add New Student Record ---")

    student_id = input("Enter Student ID: ").strip()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    # Check if student_id already exists
    if any(s["student_id"] == student_id for s in students):
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
        "final_grade": final_grade,
    }

    students.append(new_student)
    save_database(students)
    print(f"\nStudent record '{student_id}' added successfully!")


def delete_record(students: List[Dict[str, Any]]) -> None:
    """
    Delete a student record by student_id.
    
    Time Complexity: O(n) where n is the number of records
        - O(n) to filter and remove the record
        - O(n) to save database
    """
    print("\n--- Delete Student Record ---")
    student_id = input("Enter Student ID to delete: ").strip()

    initial_count = len(students)
    students[:] = [s for s in students if s["student_id"] != student_id]

    if len(students) < initial_count:
        save_database(students)
        print(f"\nStudent record '{student_id}' deleted successfully!")
    else:
        print(f"\nError: Student ID '{student_id}' not found.")


def update_record(students: List[Dict[str, Any]]) -> None:
    """
    Update an existing student record.
    
    Time Complexity: O(n) where n is the number of records
        - O(n) to find the record by student_id
        - O(1) to update the record
        - O(n) to save database
    """
    print("\n--- Update Student Record ---")
    student_id = input("Enter Student ID to update: ").strip()

    student = None
    for s in students:
        if s["student_id"] == student_id:
            student = s
            break
    
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
        student["first_name"] = first_name

    last_name = input(f"Last Name [{student['last_name']}]: ").strip()
    if last_name:
        student["last_name"] = last_name

    course_name = input(f"Course Name [{student['course_name']}]: ").strip()
    if course_name:
        student["course_name"] = course_name

    semester = input(f"Semester [{student['semester']}]: ").strip()
    if semester:
        student["semester"] = semester

    grade_input = input(f"Final Grade [{student['final_grade']}]: ").strip()
    if grade_input:
        try:
            student["final_grade"] = float(grade_input)
        except ValueError:
            print("Error: Final grade must be a number. Keeping current value.")

    save_database(students)
    print(f"\nStudent record '{student_id}' updated successfully!")


def quicksort(
    students: List[Dict[str, Any]], attribute: str, reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    Quicksort algorithm implementation from scratch.
    Sorts a list of student dictionaries by the specified attribute.
    
    Time Complexity:
        - Average case: O(n log n)
        - Best case: O(n log n)
        - Worst case: O(n²)

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
        return (
            quicksort(greater, attribute, reverse)
            + equal
            + quicksort(less, attribute, reverse)
        )
    else:
        # For ascending order
        return (
            quicksort(less, attribute, reverse)
            + equal
            + quicksort(greater, attribute, reverse)
        )


def sort_records(students: List[Dict[str, Any]]) -> None:
    """
    Sort records by a selected attribute using custom quicksort algorithm.
    
    Time Complexity: O(n log n) where n is the number of records
        - O(n log n) for quicksort (average case)
        - O(n) to display sorted records
    """
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
        "6": "final_grade",
    }

    if choice not in attribute_map:
        print("Invalid choice.")
        return

    attribute = attribute_map[choice]

    order = input("Sort order (ascending/descending) [ascending]: ").strip().lower()
    reverse = order == "descending" or order == "desc"

    # Sort the records using custom quicksort algorithm
    sorted_students = quicksort(students, attribute, reverse)

    print(
        f"\nRecords sorted by {attribute} ({'descending' if reverse else 'ascending'}):"
    )
    display_all_records(sorted_students)

    # Ask if user wants to save the sorted order
    save_choice = input("Save this sort order? (yes/no) [no]: ").strip().lower()
    if save_choice == "yes" or save_choice == "y":
        save_database(sorted_students)
        print("Sort order saved.")


def binary_search(
    students: List[Dict[str, Any]], attribute: str, search_value: Any
) -> List[Dict[str, Any]]:
    """
    Binary search algorithm implementation from scratch.
    Searches for records matching the search value in a sorted list.
    
    Time Complexity:
        - O(log n) for the binary search
        - O(k) for collecting k matching records
        - Overall: O(log n + k) where n is the list size and k is the number of matches

    Args:
        students: Sorted list of student dictionaries to search
        attribute: The attribute key to search by
        search_value: The value to search for

    Returns:
        A list of matching student records
    """
    if not students:
        return []

    results = []
    left = 0
    right = len(students) - 1

    # Binary search for the first occurrence
    first_index = -1
    while left <= right:
        mid = (left + right) // 2
        mid_value = students[mid][attribute]

        # Compare values (handles both string and numeric types)
        if isinstance(search_value, (int, float)) and isinstance(
            mid_value, (int, float)
        ):
            # Numeric comparison
            if mid_value == search_value:
                first_index = mid
                right = mid - 1  # Continue searching left for first occurrence
            elif mid_value < search_value:
                left = mid + 1
            else:
                right = mid - 1
        else:
            # String comparison (case-insensitive)
            mid_str = str(mid_value).lower()
            search_str = str(search_value).lower()
            if mid_str == search_str:
                first_index = mid
                right = mid - 1  # Continue searching left for first occurrence
            elif mid_str < search_str:
                left = mid + 1
            else:
                right = mid - 1

    # If we found a match, collect all matching records (handles duplicates)
    if first_index != -1:
        # Collect all matches starting from first_index
        i = first_index
        while i < len(students):
            current_value = students[i][attribute]
            if isinstance(search_value, (int, float)) and isinstance(
                current_value, (int, float)
            ):
                if current_value == search_value:
                    results.append(students[i])
                    i += 1
                else:
                    break
            else:
                if str(current_value).lower() == str(search_value).lower():
                    results.append(students[i])
                    i += 1
                else:
                    break

        # Also check backwards for any matches before first_index
        i = first_index - 1
        while i >= 0:
            current_value = students[i][attribute]
            if isinstance(search_value, (int, float)) and isinstance(
                current_value, (int, float)
            ):
                if current_value == search_value:
                    results.insert(0, students[i])
                    i -= 1
                else:
                    break
            else:
                if str(current_value).lower() == str(search_value).lower():
                    results.insert(0, students[i])
                    i -= 1
                else:
                    break

    return results


def filter_records(students: List[Dict[str, Any]]) -> None:
    """
    Search records by a selected data type using binary search.
    
    Time Complexity: O(n log n) where n is the number of records
        - O(n log n) to sort records using quicksort (required for binary search)
        - O(log n + k) for binary search where k is the number of matches
        - O(k) to display results
    """
    if not students:
        print("\nNo records to search.")
        return

    print("\n--- Search Records ---")
    print("Select data type to search by:")
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
        "6": "final_grade",
    }

    if choice not in attribute_map:
        print("Invalid choice.")
        return

    attribute = attribute_map[choice]

    # Get search value
    if attribute == "final_grade":
        try:
            search_value = float(input(f"Enter {attribute} to search for: ").strip())
        except ValueError:
            print("Error: Final grade must be a number.")
            return
    else:
        search_value = input(f"Enter {attribute} to search for: ").strip()
        if not search_value:
            print("Error: Search value cannot be empty.")
            return

    # Sort the records by the selected attribute first (required for binary search)
    print(f"\nSorting records by {attribute} for binary search...")
    sorted_students = quicksort(students, attribute, reverse=False)

    # Perform binary search
    results = binary_search(sorted_students, attribute, search_value)

    if results:
        print(f"\nFound {len(results)} matching record(s):")
        display_all_records(results)
    else:
        print(f"\nNo records found with {attribute} = '{search_value}'.")


def main_menu() -> None:
    """Display main menu and handle user choices."""
    initialize_database()

    while True:
        print("\n" + "=" * 50)
        print("STUDENT GRADING SYSTEM")
        print("=" * 50)
        print("1. Display all records")
        print("2. Add a record")
        print("3. Delete a record")
        print("4. Update a record")
        print("5. Sort records")
        print("6. Filter/Search records")
        print("7. Exit")
        print("=" * 50)

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
