# Async Event Processing & Notification Service

A production-grade, **async-first FastAPI microservice** for ingesting, processing, and dispatching events with strong guarantees around scalability, reliability, and observability.

---

## 1. Project Overview

### What This Project Does
This service is designed to act as a **central asynchronous event ingestion and processing system**. External systems send events to this service, which then:

- Validates and persists incoming events
- Processes them asynchronously (non-blocking)
- Tracks processing status and metadata
- Lays the foundation for webhooks, analytics, and notifications

This is **not a CRUD application**. It is an event-driven microservice focused on async workflows and production-readiness.

### Who It Is For
- Backend engineers building event-driven systems
- Teams needing a scalable event ingestion layer
- Systems requiring async processing without blocking APIs

### High-Level Workflow

1. Client sends an event to `POST /events`
2. Event is validated using Pydantic v2 schemas
3. Event metadata is stored asynchronously in PostgreSQL
4. A background task is triggered for processing
5. Processing updates event status (`pending → processed` or `failed`)
6. Logs and request IDs ensure observability

---

## 2. Features

### Core Features

- ✅ **Async Event Ingestion**
  - `POST /events` endpoint
  - Pydantic v2 validation
  - Async DB persistence

- ✅ **Async Background Processing**
  - Non-blocking background tasks
  - Simulated processing pipeline
  - Status tracking (`pending`, `processed`, `failed`)
  - Error capture in background tasks

- ✅ **Structured Logging**
  - Central JSON-style logger
  - Request ID propagation via middleware
  - Consistent log fields across layers

- ✅ **Health Check**
  - `GET /health` endpoint for service liveness

### Infrastructure & Platform

- ✅ Async SQLAlchemy (2.x) with PostgreSQL
- ✅ Redis client setup (async)
- ✅ Docker & Docker Compose for local dev
- ✅ Strict separation of concerns (routers, services, infra)

### Partially Implemented / In Progress

- 🟡 **Rate Limiting**
  - Redis-backed dependency exists
  - Refinement planned in later phases

- 🟡 **Authentication Hook**
  - Dependency wiring exists
  - API key auth implementation planned

### Planned / Not Implemented Yet

- 🔴 Webhook registration & dispatching
- 🔴 Retry logic with exponential backoff
- 🔴 Metrics & analytics endpoints
- 🔴 API key authentication enforcement
- 🔴 Authorization policies
- 🔴 Production-grade error response schemas
- 🔴 Tests (unit / integration)

---

## 3. Tech Stack

### Core Technologies
- **Language:** Python 3.11
- **Framework:** FastAPI
- **Async ORM:** SQLAlchemy 2.x (async)
- **Validation:** Pydantic v2

### Data Stores
- **Primary DB:** PostgreSQL
- **Cache / Rate Limiting:** Redis (async)

### Tooling
- Docker
- Docker Compose
- Uvicorn
- OpenAPI / Swagger (FastAPI auto-generated)

---

## 4. Project Structure

```

app/
├── main.py                 # FastAPI app entrypoint
│
├── core/
│   ├── config.py           # Pydantic-based config management
│   ├── logging.py          # Central structured logger
│   ├── exceptions.py       # Custom exception classes
│   └── security.py         # API key auth (planned / partial)
│
├── db/
│   ├── base.py             # SQLAlchemy declarative base
│   ├── session.py          # Async engine & session factory
│   └── models.py           # Event model
│
├── cache/
│   ├── redis.py            # Async Redis client
│   └── rate_limiter.py     # Redis-backed rate limiting
│
├── ingestion/
│   ├── router.py           # /events endpoint
│   ├── service.py          # Event ingestion logic
│   └── schemas.py          # Pydantic schemas
│
├── background/
│   └── tasks.py            # Async background processing
│
├── metrics/                # Created but not implemented
│
├── webhooks/               # Planned, not implemented
│
├── utils/
│   ├── ids.py              # Event / request ID generation
│   └── time.py             # Time helpers
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env

````

---

## 5. Installation & Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (via Docker)
- Redis (via Docker)

### Environment Variables
Defined via `.env` and loaded using `app/core/config.py`.

Typical variables include:
- Database connection details
- Redis connection URL
- Application-level settings

> Direct access to `os.environ` outside config is **forbidden**.

### Local Setup

```bash
docker-compose up --build
````

Service will start at:

```
http://localhost:8000
```

Health check:

```
GET /health
```

---

## 6. Usage

### Ingest an Event

```http
POST /events
Content-Type: application/json

{
  "event_type": "user.signup",
  "source": "web",
  "payload": {
    "user_id": 123
  }
}
```

### Expected Behavior

* Event is stored in DB
* Background processing is triggered
* Status transitions to `processed`
* Logs include request_id and event_id

---

## 7. Configuration

* **Single source of truth:** `app/core/config.py`
* Uses Pydantic BaseSettings
* Environment-driven
* No duplicate or inline configuration allowed

---

## 8. Architecture & Design Decisions

### Core Principles

* Async-first (no blocking calls)
* Microservice-oriented
* Strict separation of concerns
* Infrastructure code is centralized and non-duplicated

### Key Decisions

* Async SQLAlchemy only (no sync fallback)
* Single Redis client
* Central logger only
* No business logic in routers
* No FastAPI imports in services

This project follows a deliberately fixed async-first architecture with strict separation of concerns (API, services, background tasks, infrastructure).
These constraints are intentional and reflect production-style backend system design.

---

## 9. Security Considerations

### Current State

* Authentication dependencies wired
* No enforcement yet

### Planned

* API key–based authentication
* Dependency-based authorization
* No inline security checks in routers

---

## 10. Testing

### Current State

* 🔴 No automated tests implemented yet

### Planned

* Unit tests for services
* Integration tests for ingestion flow
* Async test setup with pytest

---

## 11. Performance & Optimization

### Implemented

* Fully async request handling
* Non-blocking background tasks
* Redis-backed infra components

### Planned

* Metrics caching
* Read-optimized aggregation queries
* Webhook delivery backpressure handling

---

## 12. Limitations & Known Issues

* Webhooks not implemented
* Metrics endpoints not implemented
* Authentication not enforced
* No retry or DLQ mechanism yet
* No test coverage
* Metrics directory exists but is empty

---

## 13. Roadmap / Future Improvements

* Webhook registration & dispatcher
* Retry with exponential backoff
* Delivery attempt persistence
* Metrics aggregation & caching
* Full API key security
* Observability improvements
* CI/CD pipeline
* Comprehensive test suite

---

## 14. Contribution Guidelines

* Follow async-first principles
* Do not introduce new patterns without approval
* Respect frozen architecture decisions
* Absolute imports only (`app.*`)
* Each phase must remain runnable and testable

---

## 15. License

**Not specified**

---

## Status Summary

| Area                    | Status             |
| ----------------------- | ------------------ |
| Event ingestion         | ✅ Implemented      |
| Background processing   | ✅ Implemented      |
| Logging & observability | ✅ Implemented      |
| Dockerized setup        | ✅ Implemented      |
| Rate limiting           | 🟡 Partial         |
| Security                | 🟡 Partial         |
| Webhooks                | 🔴 Planned         |
| Metrics                 | 🔴 Planned         |
| Tests                   | 🔴 Not implemented |

---

This README reflects the **actual current state** of the project, including implemented functionality, partial work, and explicitly planned components.

```
