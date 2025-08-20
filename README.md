# FactWise Python Mini Project

## Tech Stack
- Django
	-	Pros:
	    - aligns with company stack, ORM built-in, batteries included.
	-	Cons:
	    - Heavy for this small assignment.
		- Forces me into migrations, DB-style modeling (but problem states file-based persistence, not RDBMS).

- FastAPI
	-	Pros:
	    - Lightweight,
		- fast to implement REST APIs.
		- JSON I/O handling is built-in with Pydantic models → perfectly aligns with requirement.
		- Shows I can design clean, modular and production-grade APIs.
	- Assignment gives freedom of Python Library.

Hence chose FastAPI for this assignment.

## Implementations Order:
1. FileDB class (for persistent json storage)
2. Converting all base classes into Abstract classes and methods
3. Implementing Concrete User class. (Cause team and ProjectBoard will depend on it)
4. Made some unittest to check functioning of UserManager Class

## Important Commands:
- running unit tests:
```bash
python3-m unittest tests/test_user_manager.py
```
