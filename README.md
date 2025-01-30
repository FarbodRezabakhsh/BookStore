Overview
-The BookStore API is a comprehensive backend service for managing an online bookstore with a membership-based reservation system.
Built with FastAPI, PostgreSQL, and SQLAlchemy, the project implements user authentication,
book reservations, role-based access control (RBAC),
and a queue system for book reservations when stock is unavailable. This project is designed with a modular and scalable architecture,
following best practices for clean code, database normalization, and secure authentication.

Features 
-User Authentication & Authorization
-JWT-based authentication for secure access.
-Two-step login with OTP verification.
-Role-based access control (Admin, Customer, Author).
-Admins can revoke tokens and manage users.

Books & Reservations
-CRUD operations for Books, Users, Customers, Reservations.
-Instant Reservation: If a book is in stock, it is instantly reserved.
-Queued Reservation: If a book is out of stock, customers are placed in a queue.
-Prioritized Queue: Premium members get priority in the queue.

Membership & Wallet System
-Users can upgrade to Plus or Premium memberships with different benefits.
-Free users can only view books, while Plus and Premium users can reserve.
-Dynamic discount system based on previous reservations.
-Wallet system for charging and deducting balance.

Admin Functionality
-Admins can revoke user tokens.
-Admins can end reservations early.
-Admins can view and manage reservation queues.

Technologies Used 🛠️
-FastAPI - High-performance web framework.
-PostgreSQL - Relational database.
-SQLAlchemy - ORM for database interactions.
-Alembic - Database migrations.
-Pydantic - Data validation.
-Docker - Containerization support.
-Pytest - Unit testing framework.

Swagger UI: http://127.0.0.1:8000/docs