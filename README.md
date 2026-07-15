<<<<<<< HEAD
# DigiClassroom

A modern, streamlined digital classroom platform built with Django. This platform provides distinct portals for students, teachers, and administrators to facilitate digital education, track assignments, and maintain smooth communication.

## Key Features
- **Role-Based Access Control:** Dedicated dashboards and permissions for Students, Teachers, and Admins.
- **Classroom Management:** Teachers can create, manage, and distribute materials in isolated digital classrooms.
- **Assignment Tracking:** Seamlessly distribute, submit, and track assignments with built-in deadline indicators.
- **Asynchronous Notifications:** Real-time polling and dynamic alert systems for pending requests, enrollments, and support tickets.
- **Admin Support Ticketing:** Integrated helpdesk system for users to raise issues securely to administrators.

## Tech Stack
- **Backend Framework:** Django (Python)
- **Database:** SQLite3 (development) / PostgreSQL (production-ready)
- **Frontend Architecture:** Vanilla JavaScript, HTML5
- **Styling:** Custom CSS layered over Bootstrap 5, leveraging CSS variables for global theming
- **Typography:** Google Fonts (Inter) & FontAwesome Icons

## Major UI/UX Improvements
Recently overhauled to reflect a premium, resume-ready frontend:
- **Global Design System:** Transitioned to a custom Indigo/Slate color palette with modern typography and refined box-shadow implementations.
- **Glassmorphism Integration:** Upgraded navigation with translucent blur effects (`backdrop-filter`) for a premium layout.
- **Dynamic Dashboard Stats:** Rebuilt teacher and student dashboards with elegant, data-driven summary cards.
- **Asynchronous Toasts:** Replaced legacy blocking alerts with non-intrusive Bootstrap Toasts that auto-dismiss.
- **Polished Empty States:** Implemented refined empty states for lists with oversized iconography to improve user onboarding.
- **Modern Authentication:** Redesigned login, registration, and profile screens to utilize centered card layouts, floating labels, and dynamic visual grouping.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Manjita02/DigitalClassroom.git
   cd DigitalClassroom
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # OR
   .\venv\Scripts\activate   # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r digiclassrooms/requirements.txt
   ```

4. **Run migrations:**
   ```bash
   cd digiclassrooms
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

## How to Run Locally

Start the Django development server:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

## Screenshots

### 1. Dashboard View
*(A polished student/teacher dashboard showing modern stat cards and gradient course containers.)*
<br>
![Dashboard Placeholder](https://via.placeholder.com/800x400?text=Insert+Dashboard+Screenshot+Here)

### 2. Login/Register Screen
*(A sleek, centered authentication form utilizing floating labels and responsive grouping.)*
<br>
![Login Placeholder](https://via.placeholder.com/800x400?text=Insert+Login+Screenshot+Here)

### 3. Profile / Settings
*(An organized "Account Settings" layout with cleanly separated profile views and editable forms.)*
<br>
![Profile Placeholder](https://via.placeholder.com/800x400?text=Insert+Profile+Screenshot+Here)

## Suggested Future Improvements
- **Dark Mode Integration:** Implement a global toggle for dark/light themes.
- **AJAX Form Submissions:** Transition authentication and ticket submission to asynchronous forms.
- **Advanced File Handling:** Integrate AWS S3 or equivalent for robust media and assignment storage.

## License & Credits
Based on the original DigiClassroom project by ukg2005 ([Source](https://github.com/ukg2005/DigiClassroom)). 
Customized and extended by **Manjita Singh Pachora**.
This project is licensed under the MIT License - see the LICENSE file for details.
=======
# DigitalClassroom
>>>>>>> 87d59aa10bbdea12b2e1c0d09174fb99b71f2bd2
