# CLAUDE.md

# Expense Tracker Project

## Project Overview

Personal Expense Tracker Web Application built to help users:

* Record income and expenses
* Categorize transactions
* Analyze spending habits
* Generate financial reports
* Visualize financial data

This project is intended to be both a learning project and a portfolio-quality application.

---

## Technology Stack

### Backend

* Python
* Flask
* Flask-Login
* SQLAlchemy

### Database

* SQLite (current)
* PostgreSQL (future)

### Analytics

* Pandas
* Matplotlib

### Frontend

* HTML
* Jinja2 Templates
* Responsive UI (future)

---

## Portfolio Goals

This project showcases:

* Python Programming
* Data Analysis
* Full-Stack Fundamentals
* Software Architecture
* Problem Solving
* UI/UX Thinking

---

## Development Philosophy

The project is built incrementally.

For every new feature:

1. Explain the architecture first.
2. Explain how the new component connects to existing modules.
3. Implement step-by-step.
4. Prioritize understanding over speed.
5. Keep responsibilities separated.
6. Avoid large code dumps whenever possible.

---

## Coding Standards

### Type Annotations

Use return type annotations throughout the project.

Example:

```python
def dashboard() -> str:
    ...

def get_user_dataframe(
    user_id: int
) -> pd.DataFrame:
    ...
```

### Code Style

* Follow PEP 8
* Use descriptive variable names
* Prefer explicit typing
* Keep functions focused on a single responsibility

### Architecture Rules

Routes should only handle:

* HTTP requests
* HTTP responses
* Template rendering

Models should only handle:

* Database structure
* Relationships

AnalyticsService should handle:

* Pandas operations
* Aggregations
* Reports
* Data analysis

Avoid placing analytics logic directly inside routes.

---

## Current Architecture

```text
User
 │
 ▼
Routes (Flask)
 │
 ▼
Analytics Service
 │
 ▼
SQLAlchemy ORM
 │
 ▼
SQLite Database
```

### Analytics Flow

```text
User
 │
 ▼
Transaction
 │
 ▼
SQLite
 │
 ▼
Pandas DataFrame
 │
 ├── Monthly Reports
 │
 ├── Category Analysis
 │
 └── Spending Insights
 │
 ▼
Matplotlib Charts
 │
 ▼
Analytics Dashboard
```

---

## Development Roadmap

### Phase 1 — MVP

Build:

* Login system
* Add/view transactions
* SQLite database
* Basic dashboard

Status:

✅ Completed

---

### Phase 2 — Analytics

Build:

* Pandas summaries
* Monthly reports
* Visualizations

Status:

🔄 In Progress

---

### Phase 3 — Advanced Features

Build:

* CSV import/export
* Budget tracking
* Filters/search
* API endpoints

Status:

⏳ Planned

---

### Phase 4 — Production Polish

Build:

* Deployment
* Responsive UI
* Error handling
* Testing
* Documentation

Status:

⏳ Planned

---

## Current Progress

### Current Phase

Phase 2 — Analytics

### Current Step

Analytics Dashboard

### Completed

#### Phase 1

* Authentication System

* User Registration

* Password Hashing

* Login / Logout

* Session Management

* Protected Routes

* SQLite Integration

* Database Models

* Data Persistence

* Transaction Management

* Create Transactions

* View Transactions

* User Data Isolation

* Dashboard

* Income Summary

* Expense Summary

* Balance Calculation

* Transaction Metrics

#### Phase 2

* Pandas Installation
* Analytics Service Layer
* Transaction → DataFrame Pipeline
* Monthly Summary Analytics
* Category Summary Analytics
* Spending Insights
* Matplotlib Visualizations (Monthly bar chart, Category pie chart, base64 embedding)

### Next Steps

* Analytics Dashboard

---

## Development Environment

Operating System:

Windows 10

Python Environment:

venv

Run Application:

```bash
python run.py
```

Database Location:

```text
instance/expense_tracker.db
```

---

## Important Reminder

Avoid trying to make the project perfect immediately.

A completed application with:

* Authentication
* Analytics
* Documentation
* Deployment
* Clean Architecture

is significantly more valuable than an unfinished highly complex application.

Focus on completing each phase before expanding scope.
