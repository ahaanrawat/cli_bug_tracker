# CLI Bug Tracker

A lightweight, clean, and interactive Command Line Interface bug tracking tool written in Python. It features terminal styling, custom status, priority colors, and more.

## Features
- **Interactive Menu:** Easily add and manage bugs using a simple numbered system.
- **Beautiful UI:** Bugs are displayed in a readable and an aesthetically pleasing format.
- **Data Persistence:** Automatically saves and structures bugs in a local JSON database `data/bugslist.json`.
- **Input Validation:** Prevents blank entries, manages empty data states, and safely routes user input without recursive loops.

### Setup Instructions
1. *Download and unzip, cli-bug-tracker.zip to a location on your computer.*
2. *Navigate to the unzipped folder and create a virtual environment:*
   - **Mac:** `python3 -m venv venv`
   - **Linux:** `python3 -m venv venv`
   - **Windows:** `python -m venv venv`
3. *Activate the environment:*
   - **Mac:** `source venv/bin/activate`
   - **Linux** `source venv/bin/activate`
   - **Windows**: ** `venv\Scripts\activate`
4. *Install the required modules:*
   ```bash
   pip install -r requirements.txt
