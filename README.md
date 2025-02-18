---

# APDCL Attendance Registration System  

## Overview  
The **APDCL Attendance Registration System** is a web-based **Attendance Management System** developed using **Django** for Assam Power Distribution Company Limited (**APDCL**). This system streamlines attendance tracking for employees, supporting both **on-site and remote attendance marking**.  

## Features  
- **User Registration & Authentication** – Secure login and user management.  
- **Role-Based Access Control** – Three user roles: **Admin, Boss, Subordinate**.  
- **Remote Attendance Marking** – Employees can mark attendance remotely.  
- **Approval System** – Bosses can approve or reject subordinate attendance requests.  
- **Holiday Management** – Manage and track holidays effectively.  

## Technologies Used  
- **Backend**: Django (Python)  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: SQLite / PostgreSQL  
- **Deployment**: Hosted on APDCL’s internal servers  

## How to Run  
1. Clone the repository:  
   ```bash
   git clone https://github.com/DipamBhuyan/APDCL-Attendance-System.git
   cd APDCL-Attendance-System
   ```
2. Create a virtual environment and install dependencies:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run migrations:  
   ```bash
   python manage.py migrate
   ```
4. Start the Django development server:  
   ```bash
   python manage.py runserver
   ```

## Future Enhancements  
- **Mobile App Integration** for easier attendance marking.  
- **Biometric Authentication** for enhanced security.  
- **Advanced Reporting & Analytics** for attendance insights.  

## Contributors  
- **Dipam Bhuyan**
- **Dipjyoti Saikia**  

## License  
This project is for APDCL’s internal use and is not open-source.  

---
