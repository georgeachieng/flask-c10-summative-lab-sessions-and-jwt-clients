# Productivity Notes API

A secure Flask API for a productivity notes app. The backend uses session-based authentication, stores hashed passwords with `Flask-Bcrypt`, and protects every notes endpoint so users can only access their own records.

## Features

- Session auth with `POST /signup`, `POST /login`, `GET /check_session`, and `DELETE /logout`
- User-owned `Note` resource with `title`, `content`, `category`, and `user_id`
- Protected CRUD routes for notes
- Pagination on `GET /notes?page=1&per_page=10`
- Database migrations with Flask-Migrate
- Seed script with demo users and starter notes

## Project Structure

```text
.
├── client-with-jwt/
├── client-with-sessions/
├── Pipfile
├── README.md
└── server/
    ├── app.py
    ├── config.py
    ├── models.py
    ├── resources.py
    ├── seed.py
    └── migrations/
```

## Installation

1. Install dependencies:

   ```bash
   pipenv install
   ```

2. Activate the virtual environment:

   ```bash
   pipenv shell
   ```

3. Move into the backend directory:

   ```bash
   cd server
   ```

4. Set the Flask app:

   ```bash
   export FLASK_APP=app.py
   ```

5. Apply the existing migration:

   ```bash
   flask db upgrade
   ```

6. Seed the database:

   ```bash
   python seed.py
   ```

7. Start the API:

   ```bash
   python app.py
   ```

The API runs on `http://localhost:5555`, which matches the proxy configured in `client-with-sessions`.

If you change the models later, generate a new migration with:

```bash
flask db migrate -m "Describe your change"
flask db upgrade
```

## Authentication Endpoints

### `POST /signup`

Creates a new user, hashes the password, and starts a session.

### `POST /login`

Authenticates an existing user and stores `user_id` in the session.

### `GET /check_session`

Returns the current user when logged in. Returns `401` with `{}` when no session exists.

### `DELETE /logout`

Clears the server-side session.

## Notes Endpoints

### `GET /notes`

Returns the authenticated user's notes only.

Query params:

- `page` default `1`
- `per_page` default `10`, max `25`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "title": "Plan sprint demo",
      "content": "Finalize talking points and rehearse flow.",
      "category": "work",
      "created_at": "2026-04-22T10:00:00",
      "updated_at": "2026-04-22T10:00:00",
      "user_id": 1
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 1,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### `POST /notes`

Creates a note for the logged-in user.

### `GET /notes/<id>`

Returns one note owned by the logged-in user.

### `PATCH /notes/<id>`

Updates a note owned by the logged-in user.

### `DELETE /notes/<id>`

Deletes a note owned by the logged-in user.

## Demo Credentials

After seeding:

- Username: `alexdev`
- Username: `samfocus`
- Username: `tayplanner`
- Password for all demo users: `password123`

## Testing With the Provided Frontend

1. Start the Flask API on port `5555`.
2. In a separate terminal, run the session client:

   ```bash
   cd client-with-sessions
   npm install
   npm start
   ```

3. Open the React app and test signup, login, refresh persistence, and logout.
