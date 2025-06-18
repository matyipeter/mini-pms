# Property Management System (PMS)

This is a **Property Management System (PMS)** built with Django. The system allows property owners and tenants to manage properties, leases, maintenance requests, and user accounts. It provides a user-friendly interface for managing property-related operations.

## Features

### User Management
- **Custom User Model**: The system uses a custom user model (`users.User`) with roles (`owner` and `tenant`).
- **Registration**: Users can register as either an owner or a tenant using the [`RegisterForm`](users/forms.py).
- **Authentication**: Custom email-based authentication is implemented using the `EmailBackend`.
- **Login/Logout**: Users can log in and out of the system.

### Property Management
- Owners can manage their properties (CRUD operations).
- Properties are linked to leases and maintenance requests.

### Lease Management
- Owners can create leases for their properties using the [`CreateLeaseView`](lease/views.py).
- Tenants can view lease details via the [`LeaseDetailView`](lease/views.py).
- Leases can be terminated by owners.

### Maintenance Requests
- Tenants can create maintenance requests for properties they are leasing.
- Maintenance requests have statuses (`pending`, `in_progress`, `completed`).

## Project Structure

The project is organized into the following Django apps:

- **users**: Handles user authentication, registration, and profiles.
- **properties**: Manages property-related operations.
- **lease**: Manages leases between owners and tenants.
- **maintenance**: Handles maintenance requests for properties.

### Key Files and Directories

- **`pms/`**: The main project directory containing settings, URLs, and WSGI configuration.
- **`users/`**:
  - [`forms.py`](users/forms.py): Contains forms for user registration and login.
  - [`views.py`](users/views.py): Handles user-related views like registration and login.
  - [`urls.py`](users/urls.py): Defines user-related URL routes.
- **`lease/`**:
  - [`views.py`](lease/views.py): Contains views for lease management.
  - [`models.py`](lease/models.py): Defines the `Lease` model.
- **`maintenance/`**:
  - [`models.py`](maintenance/models.py): Defines the `MaintenanceRequest` model.
- **`properties/`**: Manages property-related models and views.
- **`static/`**: Contains static files like CSS, JavaScript, and images.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/matyipeter/mini-pms.git
   cd mini-pms

2. Install dependencies:
    ```sh
    pip install -r requirements.txt