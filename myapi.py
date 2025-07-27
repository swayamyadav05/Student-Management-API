from fastapi import FastAPI, Path, Query, HTTPException, status, Depends
from typing import Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict
import uuid
from contextlib import asynccontextmanager


# --- Application Lifespan Management ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application resources and clean up on shutdown"""
    # Initialize database connection, load configs, etc here
    print("Starting application...")
    yield
    # Clean up resources here
    print("Shutting down application...")


# --- Application Setup ---
app = FastAPI(
    title="Student Management API",
    description="API for managing student records",
    version="1.0.0",
    lifespan=lifespan,
)


# --- Data Models ---
class Student(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"name": "Jane Doe", "age": 15, "class_year": "year 11"}]
        }
    )

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique student identifier",
    )
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=100)
    class_year: str = Field(..., pattern=r"^year \d{1,2}$")


class UpdateStudent(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, gt=0, lt=100)
    class_: Optional[str] = Field(None, pattern=r"^year \d{1,2}$")


# --- Database Simulation ---
students_db = {
    "550e8400-e29b-41d4-a716-446655440000": Student(
        name="John", age=17, class_year="year 12"
    ),
    "f47ac10b-58cc-4372-a567-0e02b2c3d479": Student(
        name="Jane", age=16, class_year="year 11"
    ),
}


# --- Helper Functions ---
def get_student_or_404(student_id: str) -> Student:
    """Centralized student retrieval with error handling"""
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )
    return students_db[student_id]


# --- API Endpoints ---
@app.get("/", include_in_schema=False)
def root():
    """Health check endpoint (excluded from docs)"""
    return {"status": "running", "version": app.version}


@app.get(
    "/students",
    summary="Get all students",
    response_model=list[Student],
    tags=["Students"],
)
def get_all_students():
    return list(students_db.values())


@app.get(
    "/students/{student_id}",
    summary="Get student by ID",
    response_model=Student,
    tags=["Students"],
)
def get_student(student_id: str = Path(..., description="Student ID")):
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )
    return students_db[student_id]


@app.get(
    "/students/search/by-name",
    summary="Search students by name",
    response_model=list[Student],
    tags=["Students", "Search"],
)
def get_student_by_name(
    name: str = Query(..., min_length=2, description="Student name to search")
):
    results = [s for s in students_db.values() if s.name.lower() == name.lower()]
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No students found with name '{name}'",
        )
    return results


@app.post(
    "/students",
    summary="Create new student",
    response_model=Student,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
def create_student(student: Student):
    students_db[student.id] = student
    return student


@app.patch(
    "/students/{student_id}",
    summary="Update student information",
    response_model=Student,
    tags=["Students"],
)
def update_student(student_id: str, update_data: UpdateStudent):
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )

    student = students_db[student_id]
    update_dict = update_data.model_dump(exclude_unset=True)
    updated_student = student.model_copy(update=update_dict)
    students_db[student_id] = updated_student

    return updated_student


@app.delete(
    "/students/{student_id}",
    summary="Delete a student",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"],
)
def delete_student(student_id: str):
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )
    del students_db[student_id]
