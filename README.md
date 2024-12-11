# Breeze Mental Health Application

## Overview

Breeze is a comprehensive mental health management system designed to facilitate interactions between Mental Health Well-being Practitioners (MHWPs) and patients. The application provides features like appointment scheduling, mood tracking, journal management, and user-friendly summaries for practitioners and administrators.

This project is implemented in Python and designed to run as a standalone application. It includes an automated package installation process and a data seeding script (`seeder.py`) embedded within `main.py`.

---

## Installation

### Requirements

- **Python 3.10 or above**
- Ensure the `pip` package manager is installed.

---

## Getting Started

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd Breeze

Step 2: Run the Application

Simply run the following command:

python3 main.py

	•	The application will check for missing dependencies and install them automatically.
	•	If the data/users.json file does not exist, the seeder.py script will generate it with dummy data.

Application Structure

Breeze/
│
├── breeze/
│   ├── app.py                # Core application logic
│   ├── services/             # Business logic for different user roles
│   ├── models/               # User and appointment models
│   ├── utils/                # Utility functions and helpers
│
├── data/
│   ├── users.json            # Data store for users and appointments (auto-generated)
│   └── seeder.py             # Generates dummy data for development/testing
│
├── main.py                   # Entry point for the application
├── requirements.txt          # Project dependencies
└── README.md

Usage

Admin

	•	Features:
	•	View summaries of all users.
	•	Manage users (add, delete, disable, edit).

MHWP

	•	Features:
	•	View assigned patients.
	•	Access patient records (add, delete, edit conditions and prescriptions).
    •	Manage appointments with patients.

Patients

	•	Features:
	•	Log mood entries and journal entries.
    •	Book an appointment with assgiend mhwp.
    •	View hisotries (mood, journal, appointment).
    •	Seach for meditation exercises.
    •	Learn about mental conditions.


Development Details

Automated Package Installation

When you run main.py, the script checks for missing dependencies. If any are found, the requirements.txt file is used to install them. This ensures the application runs smoothly without manual package installation.

Data Seeding

	•	The seeder.py script is embedded in main.py.
	•	On the first run, it generates dummy data for users.json in the /data directory.
	•	If users.json already exists, it is overwritten to ensure a fresh start.

Important Notes

	•	Ensure you have sufficient permissions to install Python packages globally or use a virtual environment.
	•	To regenerate the users.json file, delete the existing file in /data and rerun main.py.
```
