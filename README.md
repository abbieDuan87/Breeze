# Breeze Mental Health Application

## Overview

Breeze is a comprehensive mental health management system designed to facilitate interactions between Mental Health Well-being Practitioners (MHWPs) and patients. The application provides features like appointment scheduling, mood tracking, journal management, and user-friendly summaries for practitioners and administrators.

This project is implemented purely in Python without any third-party libraries, ensuring a seamless and lightweight setup. It includes an automated data seeding script (seeder.py) embedded within main.py.

---

## Installation

### Requirements

- **Python 3.10 or above**

---

## Getting Started

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd Breeze
```

### Step 2: Run the Application

Simply run the following command:

```bash
python3 main.py
```

- The application will check for missing dependencies and install them automatically.
- If the data/users.json file does not exist, the seeder.py script will generate it with dummy data.

## Application Structure

```bash
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
└── README.md
```

### Usage

#### Admin

- Features:
  - View summaries of all users.
  - Manage users (add, delete, disable, edit).

#### MHWP

- Features:
  - View assigned patients.
  - Access patient records (add, delete, edit conditions and prescriptions).
  - Manage appointments with patients.

#### Patients

- Features:
  - Log mood entries and journal entries.
  - Book an appointment with assgiend mhwp.
  - View hisotries (mood, journal, appointment).
  - Seach for meditation exercises.
  - Learn about mental conditions.

## Development Details

### Data Seeding

- The seeder.py script is embedded in main.py.
- On the first run, it generates dummy data for users.json in the /data directory.
- If users.json already exists, it is overwritten to ensure a fresh start.

## Important Notes

- Ensure Python 3.10 or above is installed on your system.
- To regenerate the users.json file, delete the existing file in /data and rerun main.py.
- The project does not use third-party packages, ensuring a lightweight and efficient setup.
