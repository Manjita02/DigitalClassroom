# DigitalClassroom

A Django-based Learning Management System (LMS) designed for classroom management, content delivery, assessments, and streamlined communication across Admin, Teacher, and Student roles. 

## Features

- **Roles and Dashboards:** Distinct dashboards for Admin, Teacher, and Student roles with tailored workflows.
- **Classroom Management:** Secure, key-based joining for students, with role-based approval flows for new classes.
- **Lectures and Notices:** Dedicated modules for video lectures and announcements, supporting threaded discussions.
- **Assignments and Grading:**
  - Auto-grading for quizzes.
  - Manual grading for Q&A with per-question feedback.
- **Deadlines and Alerts:** Built-in calendar views and urgency-based reminders for upcoming deadlines.
- **Support and Communication:** Integrated ticketing system and threaded support conversations.

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (default, compatible with PostgreSQL/MySQL)
- **Frontend:** HTML5, CSS3, Django Template Language
- **Authentication:** Django's built-in authentication system with custom profiles

## Prerequisites

- Python 3.x
- pip (Python package installer)
- virtualenv (recommended)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Manjita02/DigitalClassroom.git
   cd DigitalClassroom
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r digiclassrooms/requirements.txt
   ```
   *(Note: Adjust the path to `requirements.txt` if necessary based on the project structure)*

4. **Run migrations:**
   ```bash
   python digiclassrooms/manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python digiclassrooms/manage.py runserver
   ```

## Usage Instructions

- Navigate to `http://127.0.0.1:8000` in your web browser.
- **Admin Access:** You can create a superuser using `python digiclassrooms/manage.py createsuperuser` to access the admin dashboard.
- **Students/Teachers:** Register an account via the web interface. Teachers can create classes and generate join keys, which students can use to enroll.

## Credits

Based on DigiClassroom by ukg2005 (https://github.com/ukg2005/DigiClassroom).
Customized and extended by **Manjita Singh Pachora** <manjitasinghpachora@gmail.com>.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
