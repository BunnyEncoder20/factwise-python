# FactWise Python Mini Project

A team project planner tool with REST APIs for managing users, teams, and project boards with task management capabilities.

## Overview

This project implements a comprehensive project management system that allows:
- **User Management**: Create, update, list, and manage users
- **Team Management**: Create teams, add/remove members, and manage team hierarchies
- **Project Board Management**: Create boards, manage tasks, and track project progress

The application uses file-based JSON storage for persistence and provides a clean REST API interface.

## Tech Stack & Architecture Decision

### Why FastAPI?
After evaluating Django vs FastAPI:

**Django**:
- ✅ Aligns with company stack, ORM built-in, batteries included
- ❌ Too heavy for this assignment
- ❌ Forces migrations and DB-style modeling (requirement specifies file-based persistence)

**FastAPI**:
- ✅ Lightweight and fast for REST API implementation
- ✅ Built-in JSON I/O with Pydantic models (perfect for requirements)
- ✅ Demonstrates clean, modular, production-grade API design
- ✅ Assignment allows freedom of Python library choice

**Decision**: Chose FastAPI for optimal alignment with requirements.

## Project Structure

```
factwise-python/
├── abstract_classes/          # Base abstract classes
├── impl/                      # Concrete implementations
├── app/                       # FastAPI application
├── tests/                     # Unit tests
├── db/                        # JSON file storage (created at runtime)
└── requirements.txt           # Dependencies
```

## Implementation Approach

1. **FileDB Class**: JSON-based persistent storage system
2. **Abstract Base Classes**: Converted provided classes to proper abstract classes
3. **User Manager**: Core implementation (dependency for teams and boards)
4. **Unit Testing**: Comprehensive testing for UserManager functionality
5. **Team Manager**: Team creation and member management
6. **Board Manager**: Project boards and task management
7. **REST API Layer**: FastAPI wrapper for all business logic
8. **API Testing**: Comprehensive testing via Postman

## Data Models

### User Schema
```json
{
  "id": "uuid4()",
  "name": "string",
  "display_name": "string",
  "description": "string",
  "creation_time": "ISO datetime"
}
```

### Team Schema
```json
{
  "id": "uuid4()",
  "name": "string",
  "description": "string",
  "admin": "user_id",
  "users": ["user_id1", "user_id2"],
  "creation_time": "ISO datetime"
}
```

### Board & Task Schema
```json
{
  "board": {
    "id": "uuid4()",
    "name": "string",
    "description": "string",
    "team_id": "team_id",
    "creation_time": "ISO datetime",
    "end_time": "ISO datetime | null",
    "status": "OPEN | CLOSED"
  },
  "task": {
    "id": "uuid4()",
    "title": "string",
    "description": "string",
    "user_id": "assigned_user_id",
    "creation_time": "ISO datetime",
    "status": "OPEN | IN_PROGRESS | COMPLETE"
  }
}
```

## Setup & Installation

### Prerequisites
- Python 3.7+
- pip or uv package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/BunnyEncoder20/factwise-python
   cd factwise-python
   ```

2. **Install dependencies**
   ```bash
   # Using pip
   pip install -r requirements.txt

   # Or using uv (faster)
   uv pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the API**
   - **API Server**: http://127.0.0.1:8000
   - **Swagger UI**: http://127.0.0.1:8000/docs
   - **ReDoc**: http://127.0.0.1:8000/redoc

5. **Testing with Postman**
    - Have include the Postman collection of the project within the 'postman collection' dir
    ```bash
    ./'postman collection'/'FactWise Assignment Project.postman_collection.json'
    ```
    - These can imported directly into Postman

### Testing

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests/test_user_manager.py
```

## Key Design Decisions & Assumptions

### File-based Storage
- JSON files stored in `db/` directory (auto-created)
- Each entity type (users, teams, boards) has separate JSON files
- Thread-safe file operations with proper locking

### Abstract Class Enhancement
- Enhanced provided abstract classes with proper `@abstractmethod` decorators
- Added missing method signatures for complete API coverage

### Add Task Method Fix
- **Issue**: Original `add_task` method in `project_board_base` had incomplete parameters
- **Solution**: Added required `board_id` and `user_id` parameters
- **Rationale**: Tasks must be associated with specific boards and assigned to users

### UUID Generation
- All entities use UUID4 for unique identification
- Ensures no ID conflicts and better scalability

### Error Handling
- Comprehensive exception handling for invalid inputs
- Proper HTTP status codes returned via FastAPI
- Detailed error messages for debugging

## API Features

- **RESTful Design**: Follows REST conventions
- **Input Validation**: Pydantic models ensure data integrity
- **Error Handling**: Consistent error responses
- **Documentation**: Auto-generated OpenAPI docs
- **Testing**: Comprehensive unit test coverage of business logic
