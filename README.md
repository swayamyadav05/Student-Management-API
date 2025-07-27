# Student Management API

A RESTful API built with FastAPI for managing student records. This project demonstrates core FastAPI concepts including data models, validation, CRUD operations, and API documentation.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete student records
- **Data Validation**: Input validation using Pydantic models
- **Search Functionality**: Search students by name
- **Auto Documentation**: Interactive API docs with Swagger UI
- **Error Handling**: Proper HTTP status codes and error messages
- **Application Lifespan**: Graceful startup and shutdown handling

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Python 3.12**: Programming language
- **UUID**: Unique identifier generation

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/swayamyadav05/Student-Management-API.git
   cd FastAPI
   ```

2. **Install dependencies**

   ```bash
   pip install fastapi uvicorn
   ```

3. **Run the application**

   ```bash
   uvicorn myapi:app --reload
   ```

4. **Access the API**
   - API Base URL: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc Documentation: http://localhost:8000/redoc

## API Endpoints

### Students

| Method | Endpoint                               | Description        | Status Code |
| ------ | -------------------------------------- | ------------------ | ----------- |
| GET    | `/`                                    | Health check       | 200         |
| GET    | `/students`                            | Get all students   | 200         |
| GET    | `/students/{student_id}`               | Get student by ID  | 200, 404    |
| GET    | `/students/search/by-name?name={name}` | Search by name     | 200, 404    |
| POST   | `/students`                            | Create new student | 201         |
| PATCH  | `/students/{student_id}`               | Update student     | 200, 404    |
| DELETE | `/students/{student_id}`               | Delete student     | 204, 404    |

## Data Models

### Student Model

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "age": 17,
  "class_year": "year 12"
}
```

### Validation Rules

- **name**: 2-50 characters
- **age**: 1-99 years
- **class_year**: Must match pattern "year X" (e.g., "year 11", "year 12")

## Usage Examples

### Create a Student

```bash
curl -X POST "http://localhost:8000/students" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Alice Smith",
       "age": 16,
       "class_year": "year 11"
     }'
```

### Get All Students

```bash
curl -X GET "http://localhost:8000/students"
```

### Search by Name

```bash
curl -X GET "http://localhost:8000/students/search/by-name?name=John"
```

### Update a Student

```bash
curl -X PATCH "http://localhost:8000/students/{student_id}" \
     -H "Content-Type: application/json" \
     -d '{
       "age": 18
     }'
```

## Key Features Demonstrated

### 1. **Data Validation**

- Pydantic models with field validation
- Custom regex patterns for class year
- Optional fields for updates

### 2. **Error Handling**

- HTTP 404 for missing resources
- Descriptive error messages
- Proper status codes

### 3. **Application Lifespan**

- Startup and shutdown event handling
- Resource initialization and cleanup

### 4. **API Documentation**

- Automatic OpenAPI schema generation
- Custom examples and descriptions
- Organized with tags

## Development Notes

- **In-Memory Database**: Uses a dictionary for data storage (not persistent)
- **UUID Generation**: Automatic unique ID creation for new students
- **Path Parameters**: Student ID validation in URL paths
- **Query Parameters**: Name search with validation
- **Response Models**: Type-safe API responses

## Enhancements You Can Try

- [ ] Add database persistence (PostgreSQL/MongoDB)
- [ ] Implement authentication and authorization
- [ ] Add pagination for student lists
- [ ] Include more search filters (age, class year)
- [ ] Add bulk operations
- [ ] Implement data export functionality
- [ ] Add logging and monitoring

## Learning Objectives

This project covers:

- FastAPI application structure
- RESTful API design principles
- Data validation with Pydantic
- HTTP status codes and error handling
- API documentation best practices
- Python type hints and modern syntax

## License

This project is for educational purposes. Feel free to use and modify as needed.

---

**Author**: Swayam Yadav
**Created**: 2025-07-27
**FastAPI Version**: 0.104+  
**Python Version**: 3.12+
