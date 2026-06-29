import json
import sys

from pathlib import Path
from rich.console import Console
from rich.table import Table, box

console = Console()

SOURCE_FOLDER = Path(__file__).parent
MAIN_FOLDER = SOURCE_FOLDER.parent
DATA_PATH = MAIN_FOLDER / "data" / "bugslist.json"

STATUS_MAP = {
    "1": "On hold",
    "2": "In progress",
    "3": "Completed"
}

PRIORITY_MAP = {
    "1": "Low",
    "2": "Medium",
    "3": "High",
    "4": "Critical"
}

STATUS_COLORS = {
    "Completed": "#009903",
    "In progress": "#dfaf87",
    "On hold": "#afafaf"
}

PRIORITY_COLORS = {
    "Critical": "#870000",
    "High": "#cf0000",
    "Medium": "#cf6b00",
    "Low": "#009903"
}

def load_bugs_data():
    try:
        with open(DATA_PATH) as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: File not found, please check the file path and try again.")
    except json.JSONDecodeError:
        print("Error: Invalid syntax in JSON file, please check your file for any errors and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def check_first_time(all_bugs):
    return all_bugs is None or not all_bugs

def greetings(is_first_time):
    print("\n\nCommand Line Interface Bug Tracker\n")
    
    if is_first_time:
        print("1. Add your first bug")
    else:
        print("1. Add a new bug")
    
    print("2. View all bugs")
    print("3. Update a bug")
    print("4. Clear all bugs")
    print("5. Exit\n\n")
    
    user_response = input("Please select an option number (1-5):\n> ")
    return user_response

def go_back_option():
    print("\n")
    go_back = input("Go back (Y/n)\n> ")
    
    if go_back.lower() == "y":
        main()

def get_status_input():
    while True:
        print("\nBug status?\n")
        print("1. On hold")
        print("2. In progress")
        print("3. Completed")
        
        status = input("\nPlease select an option number (1-3):\n> ")
        
        if status in STATUS_MAP:
            return STATUS_MAP[status]
        print("Invalid selection. Please try again.")

def get_priority_input():
    while True:
        print("\nBug priority?\n")
        print("1. Low")
        print("2. Medium")
        print("3. High")
        print("4. Critical")
        
        priority = input("\nPlease select an option number (1-4):\n> ")
        
        if priority in PRIORITY_MAP:
            return PRIORITY_MAP[priority]
        print("Invalid selection. Please try again.")

def add_bugs():
    name = input("\nBug name\n> ").strip()

    if not name:
        print("Bug name cannot be empty.")
        return None
    
    status = get_status_input()
    priority = get_priority_input()
    
    return name, status, priority

def save_bugs_data(all_bugs):
    try:
        with open(DATA_PATH, 'w') as file:
            json.dump(all_bugs, file, indent=4)
            return True
    except Exception as e:
        print(f"Failed to save data: {e}")
        return False

def get_colored_text(text, color_map):
    color = color_map.get(text, None)
    if color:
        return f"[{color}]{text}[/{color}]"
    return text

def view_all_bugs(all_bugs):
    table = Table(
        title="All Bugs\n",
        show_header=True,
        box=box.SIMPLE_HEAD
    )
    
    if not all_bugs:
        print("\nNo bugs to view!")
        return
    
    table.add_column("Name")
    table.add_column("Status")
    table.add_column("Priority")
    
    for bug_dictionary in all_bugs:
        for bug_name, details in bug_dictionary.items():
            status_text = details.get('status', 'Unknown')
            priority_text = details.get('priority', 'Unknown')
            
            colored_status = get_colored_text(status_text, STATUS_COLORS)
            colored_priority = get_colored_text(priority_text, PRIORITY_COLORS)
            
            table.add_row(bug_name, colored_status, colored_priority)
    
    console.print(table)
    print("\n")

def clear_all_bugs():
    print('\n')
    clear_bugs_input = input("Are you sure you want to clear all bugs? (Y/n)\n> ")
    return clear_bugs_input.lower() == 'y'

def get_update_details():
    status = get_status_input()
    priority = get_priority_input()
    return status, priority

def update_bugs(all_bugs):
    if not all_bugs:
        print("No bugs to update")
        return
    
    view_all_bugs(all_bugs)
    bug_name = input("\nType the name of the bug you want to update\n> ").strip()
    
    for bug_dictionary in all_bugs:
        if bug_name in bug_dictionary:
            new_status, new_priority = get_update_details()
            bug_dictionary[bug_name]['status'] = new_status
            bug_dictionary[bug_name]['priority'] = new_priority
            
            save_bugs_data(all_bugs)
            print(f"\nUpdated bug: {bug_name}")
            return
    
    print(f"\nBug '{bug_name}' not found.")

def main():
    while True:
        all_bugs = load_bugs_data()
        is_first_time = check_first_time(all_bugs)
        user_response = greetings(is_first_time)

        if all_bugs is None:
            all_bugs = []
    
        if user_response == "1":
            result = add_bugs()
            if result:
                bug_name, bug_status, bug_priority = result
                all_bugs.append({
                    bug_name: {
                        'status': bug_status,
                        'priority': bug_priority
                    }
                })
                save_bugs_data(all_bugs)
                print("Bug added.")
            go_back_option()

        elif user_response == "2":
            view_all_bugs(all_bugs)
            go_back_option()

        elif user_response == "3":
            update_bugs(all_bugs)
            go_back_option()

        elif user_response == "4":
            if clear_all_bugs():
                all_bugs = []
                save_bugs_data(all_bugs)
                print("All data successfully deleted")
            else:
                print("Cancelled")
            go_back_option()

        elif user_response == "5":
            print("Exited program.")
            sys.exit()
        else:
            print("Invalid selection. Please try again.")
            main()
    
if __name__ == "__main__":
    main()
