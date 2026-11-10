# E-Commerce Microservices Security System

### JWT Authentication and Role-Based Access Control (RBAC)

## Project Overview

This project demonstrates the implementation of **JWT-based authentication and Role-Based Access Control (RBAC)** in an e-commerce application.

The system simulates four microservices: Product, Customer, Order, and Payment. It prevents unauthorized users from accessing restricted APIs based on their assigned roles.

## Technologies Used

- **Python** – Backend programming
- **Flask** – REST API development
- **PyJWT** – JWT authentication
- **HTML & CSS** – Web interface
- **JavaScript** – API communication and user interaction

## Features

- JWT-based user authentication
- Role-based authorization
- ADMIN, SELLER, and CUSTOMER roles
- Protected REST API endpoints
- Unauthorized access prevention
- HTTP status code handling (200, 401, 403)
- Interactive web interface for API testing

## Role-Based Permissions

| Feature | ADMIN | SELLER | CUSTOMER |
|---|---|---|---|
| View Products | Yes | Yes | Yes |
| Add Products | Yes | Yes | No |
| Delete Products | Yes | Own Only | No |
| View Orders | All | Related | Own |
| Make Payment | No | No | Yes |
| Manage Users | Yes | No | No |

## Project Structure

```text
SOA_InSem2/
├── app.py
├── requirements.txt
├── README.md
└── templates/
    └── index.html
```

## Installation and Execution

**1. Clone the repository**

```bash
git clone <repository-url>
cd SOA_InSem2
```

**2. Install dependencies**

```bash
python3 -m pip install -r requirements.txt
```

**3. Run the application**

```bash
python3 app.py
```

**4. Open the application**

Visit:

http://127.0.0.1:5000/

## Demo Login Credentials

| Role | Username | Password |
|---|---|---|
| ADMIN | admin | admin123 |
| SELLER | seller | seller123 |
| CUSTOMER | customer | customer123 |

*These credentials are for local demonstration purposes only.*

## API Endpoints

| Method | Endpoint | Authorized Roles |
|---|---|---|
| POST | `/login` | Public |
| GET | `/products` | All roles |
| POST | `/products/add` | ADMIN, SELLER |
| DELETE | `/products/<product_id>` | ADMIN, owning SELLER |
| GET | `/orders` | All roles (filtered by ownership) |
| POST | `/payment` | CUSTOMER |
| GET | `/admin/users` | ADMIN |

## Security Implementation

1. Users log in with their credentials.
2. The server generates a JWT containing the user's identity, role, and expiration time.
3. The JWT is sent with subsequent API requests.
4. Flask verifies the token and checks the user's role.
5. Authorized requests are processed.
6. Unauthorized requests are rejected with appropriate HTTP status codes.

## Testing Results

| Test Case | Expected Result |
|---|---|
| ADMIN accessing Admin API | 200 OK |
| SELLER adding a product | 200 OK |
| CUSTOMER accessing Admin API | 403 Forbidden |
| Request without JWT | 401 Unauthorized |
| Invalid JWT | 401 Unauthorized |

## Limitations

This project is an educational prototype. The four microservices are simulated within a single Flask application rather than deployed independently.

HTTPS/mTLS-based inter-service communication is not implemented. User credentials and JWT secrets are hardcoded for demonstration purposes and must be secured in a production environment.

## Conclusion

The project successfully demonstrates JWT authentication, role-based authorization, and API access restrictions in an e-commerce application.

It illustrates how RBAC prevents unauthorized users from accessing administrative functionality, even when they modify API URLs.

---

**Project Type:** Service-Oriented Architecture (SOA) Lab

**Implementation:** Python Flask, JWT, HTML, CSS, JavaScript