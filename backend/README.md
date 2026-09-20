# HelioSL Backend

FastAPI backend for the HelioSL Agentic AI Renewable Energy
Intelligence Platform.

## Requirements

- Python 3.11+
- PostgreSQL 16
- Docker (recommended)

## Setup

Create environment:

```bash
python3 -m venv .venv
source .venv/bin/activate

## Core Data Model

HelioSL currently manages:

- Users
- Energy profiles
- Monthly electricity consumption
- Solar systems
- Monthly solar generation

## Main API Groups

- `/api/v1/users`
- `/api/v1/energy`
- `/api/v1/solar`
- `/api/v1/health`

## Run Development Server

```bash
python -m uvicorn app.main:app --reload

## Authentication

HelioSL uses JWT-based authentication.

### Register

`POST /api/v1/auth/register`

### Login

`POST /api/v1/auth/login`

### Current User

`GET /api/v1/auth/me`

Protected endpoints require:

```text
Authorization: Bearer <access_token>