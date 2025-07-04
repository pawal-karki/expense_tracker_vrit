# Django Expense Tracker API

A REST API for expense and income tracking built with Django REST Framework. Features JWT authentication with email verification, user access control, and tax calculations.

## Features

- JWT Authentication with email verification
- User access control (regular users see own records, superusers see all)
- Complete CRUD operations for expenses and income
- Tax calculation (flat rate and percentage-based)
- Paginated API responses (20 items per page)
- Email verification system with 15-minute expiry
- Token refresh and blacklisting for security
- User financial summary endpoint
- Filter by transaction type (debit/credit)

## Technology Stack

- Backend: Django 5.2.4
- API Framework: Django REST Framework 3.15.2
- Authentication: JWT (djangorestframework-simplejwt 5.3.0)
- Database: SQLite (development)
- Python: 3.13+

## Requirements

- Python 3.13+
- Virtual environment (recommended)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd expensetracker
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Navigate to Django Project

```bash
cd expense_tracker
```

### 6. Run Database Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Start Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication Endpoints

| Method | Endpoint                     | Description               |
| ------ | ---------------------------- | ------------------------- |
| POST   | `/auth/register/`            | User registration         |
| POST   | `/auth/login/`               | User login                |
| POST   | `/auth/refresh/`             | Refresh JWT token         |
| POST   | `/auth/verify-email/`        | Verify email address      |
| POST   | `/auth/resend-verification/` | Resend verification email |

### Expense/Income Endpoints

| Method | Endpoint                     | Description                   |
| ------ | ---------------------------- | ----------------------------- |
| GET    | `/api/expenses/`             | List all expenses (paginated) |
| POST   | `/api/expenses/create/`      | Create new expense/income     |
| GET    | `/api/expenses/{id}/`        | Get specific expense          |
| PUT    | `/api/expenses/{id}/update/` | Update expense                |
| DELETE | `/api/expenses/{id}/delete/` | Delete expense                |
| GET    | `/api/expenses/type/{type}/` | Filter by type (debit/credit) |

## Tax Calculation System

The API supports two tax calculation methods:

### Flat Tax

```json
{
  "amount": 100.0,
  "tax": 10.0,
  "tax_type": "flat"
}
```

Total: 100.00 + 10.00 = 110.00

### Percentage Tax

```json
{
  "amount": 100.0,
  "tax": 10.0,
  "tax_type": "percentage"
}
```

Total: 100.00 + (100.00 × 10 ÷ 100) = 110.00

## Authentication Flow

### 1. User Registration

```bash
curl -X POST http://localhost:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "pawaltest",
    "email": "pawal@test.com",
    "password": "pawal123",
    "password_confirm": "pawal123",
    "first_name": "Pawal",
    "last_name": "Karki"
  }'
```

### 2. Email Verification

Check your terminal output for the verification link and visit it to activate your account.

### 3. User Login

```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "pawaltest",
    "password": "pawal123"
  }'
```

### 4. Use Access Token

```bash
curl -X GET http://localhost:8000/api/expenses/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Creating Expenses/Income

### Create Expense

```bash
curl -X POST http://localhost:8000/api/expenses/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Office Supplies",
    "description": "Pens, papers, and notebooks",
    "amount": 25.50,
    "transaction_type": "debit",
    "tax": 5.00,
    "tax_type": "flat"
  }'
```

### Create Income

```bash
curl -X POST http://localhost:8000/api/expenses/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Freelance Payment",
    "description": "Web development project",
    "amount": 500.00,
    "transaction_type": "credit",
    "tax": 15.00,
    "tax_type": "percentage"
  }'
```

## Update Expense/Income

Update an existing expense:

```bash
curl -X PUT http://localhost:8000/api/expenses/1/update/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Office Supplies",
    "description": "Updated description - more office items",
    "amount": 35.75,
    "transaction_type": "debit",
    "tax": 7.50,
    "tax_type": "flat"
  }'
```

Response:

```json
{
  "id": 1,
  "title": "Updated Office Supplies",
  "description": "Updated description - more office items",
  "amount": "35.75",
  "transaction_type": "expense",
  "tax": "7.50",
  "tax_type": "flat",
  "total_amount": "43.25",
  "created_at": "2025-01-04T15:30:00Z",
  "updated_at": "2025-01-04T16:45:00Z",
  "message": "success",
  "status": 200
}
```

## Delete Expense/Income

Delete an expense:

```bash
curl -X DELETE http://localhost:8000/api/expenses/1/delete/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:

```json
{
  "message": "Expense deleted successfully",
  "status": 204
}
```

## Get Specific Expense

Retrieve a specific expense by ID:

```bash
curl -X GET http://localhost:8000/api/expenses/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:

```json
{
  "id": 1,
  "title": "Office Supplies",
  "description": "Pens, papers, and notebooks",
  "amount": "25.50",
  "transaction_type": "expense",
  "tax": "5.00",
  "tax_type": "flat",
  "total_amount": "30.50",
  "created_at": "2025-01-04T15:30:00Z",
  "updated_at": "2025-01-04T15:30:00Z",
  "message": "success",
  "status": 200
}
```

## List All Expenses

Get paginated list of expenses:

```bash
curl -X GET http://localhost:8000/api/expenses/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:

```json
{
  "count": 15,
  "next": "http://localhost:8000/api/expenses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Office Supplies",
      "description": "Pens, papers, and notebooks",
      "amount": "25.50",
      "transaction_type": "expense",
      "tax": "5.00",
      "tax_type": "flat",
      "total_amount": "30.50",
      "created_at": "2025-01-04T15:30:00Z",
      "updated_at": "2025-01-04T15:30:00Z"
    }
  ],
  "message": "success",
  "status": 200
}
```

## Filter by Transaction Type

Get only debits (expenses):

```bash
curl -X GET http://localhost:8000/api/expenses/type/debit/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Get only credits (income):

```bash
curl -X GET http://localhost:8000/api/expenses/type/credit/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Error Handling Examples

### 403 Forbidden - Permission Denied

These scenarios will return 403 Forbidden errors:

#### 1. Access Another User's Expense

Try to access an expense that belongs to another user:

```bash
curl -X GET http://localhost:8000/api/expenses/999/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:

```json
{
  "detail": "You do not have permission to perform this action.",
  "status": 403
}
```

#### 2. Update Another User's Expense

Try to update an expense that doesn't belong to you:

```bash
curl -X PUT http://localhost:8000/api/expenses/999/update/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Trying to hack",
    "amount": 100.00,
    "transaction_type": "debit"
  }'
```

Response:

```json
{
  "detail": "You do not have permission to perform this action.",
  "status": 403
}
```

#### 3. Delete Another User's Expense

Try to delete an expense that belongs to another user:

```bash
curl -X DELETE http://localhost:8000/api/expenses/999/delete/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:

```json
{
  "detail": "You do not have permission to perform this action.",
  "status": 403
}
```

### 401 Unauthorized - Missing Authentication

These scenarios will return 401 Unauthorized errors:

#### 1. Access Protected Endpoint Without Token

```bash
curl -X GET http://localhost:8000/api/expenses/
```

Response:

```json
{
  "detail": "Authentication credentials were not provided.",
  "status": 401
}
```

#### 2. Use Invalid or Expired Token

```bash
curl -X GET http://localhost:8000/api/expenses/ \
  -H "Authorization: Bearer invalid_token_here"
```

Response:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "status": 401
}
```

### 404 Not Found

Try to access a non-existent expense:

```bash
curl -X GET http://localhost:8000/api/expenses/99999/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:

```json
{
  "detail": "Not found.",
  "status": 404
}
```

### 400 Bad Request - Validation Errors

#### 1. Missing Required Fields

```bash
curl -X POST http://localhost:8000/api/expenses/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Missing title and amount"
  }'
```

Response:

```json
{
  "title": ["This field is required."],
  "amount": ["This field is required."],
  "transaction_type": ["This field is required."],
  "status": 400
}
```

#### 2. Invalid Transaction Type

```bash
curl -X POST http://localhost:8000/api/expenses/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test",
    "amount": 100.00,
    "transaction_type": "invalid_type"
  }'
```

Response:

```json
{
  "transaction_type": ["\"invalid_type\" is not a valid choice."],
  "status": 400
}
```

## Security Features

- JWT Token Authentication with 60-minute access token lifetime
- Token Refresh with 1-day refresh token lifetime
- Token Rotation - new refresh token on each refresh
- Token Blacklisting - old tokens invalidated
- Email Verification required before login
- User Isolation - users can only access their own data
- Superuser Access - admin users can access all data

## Data Models

### User Model (Django Built-in)

- username, email, first_name, last_name
- is_active, is_superuser

### ExpenseIncome Model

- user (ForeignKey to User)
- title (CharField, max 200)
- description (TextField, optional)
- amount (DecimalField, 2 decimal places)
- transaction_type (Choice: 'debit' or 'credit')
- tax (DecimalField, 2 decimal places)
- tax_type (Choice: 'flat' or 'percentage')
- created_at, updated_at (auto timestamps)

### EmailVerification Model

- user (OneToOneField)
- verification_key (UUIDField)
- created_at (DateTimeField)
- is_verified (BooleanField)

## Testing

Run the test suite:

```bash
python manage.py test
```

Test specific apps:

```bash
# Test authentication
python manage.py test authentication

# Test expenses
python manage.py test expenses
```

## Development Notes

### Email Verification in Development

Email verification links are displayed in the terminal console during development. In production, configure proper email backend in `settings.py`.

### Token Lifetimes

- Access Token: 60 minutes
- Refresh Token: 1 day
- Email Verification: 15 minutes

### Pagination

All list endpoints return paginated results with 20 items per page. Use `?page=2` parameter for pagination.

## Configuration

Key settings in `expense_tracker/settings.py`:

```python
# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Pagination
REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
}
```

## License

This project is developed for educational purposes as part of an internship task.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For questions or issues, please check the API endpoints documentation or review the error responses for debugging information.
