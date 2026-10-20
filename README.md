# Vacation Lookup API

A simple web application to track and check user vacation status.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Server

```bash
python server.py
```

The server will start on port 3000 (or the PORT environment variable if set).

## API Endpoints

### 1. Set Vacation

**POST** `/vacation`

Set a vacation date for a user.

**Request Body:**
```json
{
  "username": "john",
  "date": "2026-05-12"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Vacation set for john on 2026-05-12"
}
```

**Example:**
```bash
curl -X POST http://localhost:3000/vacation \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "date": "2026-05-12"}'
```

### 2. Check Vacation Status

**GET** `/vacation/:username`

Check if a user is on vacation today.

**Response:**
```json
{
  "username": "john",
  "onVacation": "yes",
  "vacationDate": "2026-05-12"
}
```

Returns "yes" if the user's vacation date matches today's date, otherwise "no".

**Example:**
```bash
curl http://localhost:3000/vacation/john
```

## Database

Uses SQLite (via SQLAlchemy) with a single table `vacations`:
- `username` (TEXT, PRIMARY KEY)
- `vacation_date` (TEXT)

The database file (`vacations.db`) is created automatically on first run.
