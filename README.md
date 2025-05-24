# Store API

FastAPI-based store API with PostgreSQL, Redis, and Docker support.

## Features

- User authentication with JWT
- Role-based access control (admin/user)
- Product management with categories and variations
- Order management
- File uploads
- Rate limiting
- Caching with Redis
- Email notifications
- Docker support
- CI/CD with GitHub Actions

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/store-api.git
cd store-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:

First, create `.env.example` file in the root directory:
```bash
touch .env.example
```

Then, add the following content to `.env.example`:
```env
# Database settings
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=store_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis settings
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# JWT settings
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS settings
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# File upload settings
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=5242880  # 5MB in bytes

# Logging settings
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Rate limiting
RATE_LIMIT_PER_MINUTE=60

# Email settings (optional)
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAILS_FROM_EMAIL=your-email@gmail.com
EMAILS_FROM_NAME=Store Admin

# Admin user settings
FIRST_ADMIN_EMAIL=admin@example.com
FIRST_ADMIN_PASSWORD=admin123
FIRST_ADMIN_FULL_NAME=Admin User
```

Finally, create your `.env` file:
```bash
cp .env.example .env
# Edit .env file with your settings
nano .env
```

5. Initialize the database:
```bash
alembic upgrade head
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

## Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Project Structure

```
store-api/
├── alembic/              # Database migrations
├── app/
│   ├── api/             # API endpoints
│   ├── core/            # Core functionality
│   ├── crud/            # Database operations
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── main.py          # Application entry point
├── tests/               # Test files
├── .env.example         # Example environment variables
├── .env                 # Your environment variables (create from .env.example)
├── docker-compose.yml   # Docker configuration
└── requirements.txt     # Python dependencies
```

### Running Tests

```bash
pytest
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting

## License

MIT 