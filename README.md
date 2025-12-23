# Async Event Processing & Notification Service

Production-grade, async-first FastAPI microservice for event ingestion,
background processing, analytics, and reliable notifications.

This is **NOT** a CRUD application.

---

## Architecture Overview

- Async-first FastAPI service
- Background event processing
- Redis-backed caching & rate limiting
- PostgreSQL (async SQLAlchemy 2.x)
- Structured JSON logging with request ID propagation

Designed for **scalability, reliability, and observability**.

---

## Tech Stack

- Python 3.11
- FastAPI
- Async SQLAlchemy 2.x
- PostgreSQL
- Redis
- Pydantic v2
- Docker & Docker Compose

---

## Core Capabilities

- Event ingestion with validation
- Asynchronous background processing
- Webhook delivery with retries & backoff
- Metrics aggregation with Redis caching
- API-key based authentication
- Dependency-based rate limiting
- Centralized structured logging

---

## Running Locally

```bash
docker-compose up --build
````

Service will be available at:

* API: [http://localhost:8000](http://localhost:8000)
* Health: [http://localhost:8000/health](http://localhost:8000/health)
* OpenAPI Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Documentation

Interactive OpenAPI documentation is available via Swagger UI:

```text
GET /docs
```

All request/response schemas are generated directly from Pydantic v2 models.

---

## Performance Considerations

* Fully async request handling
* No blocking I/O
* Background tasks executed via asyncio
* Redis used for read-optimized metrics
* Connection pooling for DB & Redis

---

## Deployment Notes

* Designed for containerized environments
* Horizontal scaling supported
* Stateless API layer
* Externalized config via environment variables

---

## Project Governance

* Phase-driven implementation
* Frozen architecture & decisions
* No deviation without explicit approval
