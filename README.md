# Flask-ToDo-List

A minimal Flask to-do application using SQLite. Each task can have a due time and
the interface allows toggling completion **within one hour after it is due**.

## Requirements
- Python 3.11
- See `requirements.txt` for Python packages.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Open your browser at <http://localhost:5000>.

If you run this version against an existing database created before the due-time
feature, the application will automatically add the missing column at startup.

When adding a task you must also provide a due date and time. Tasks can be
toggled complete **only within the hour after they are due**.
