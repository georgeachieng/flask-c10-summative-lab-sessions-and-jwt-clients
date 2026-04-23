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

## Endpoint Testing Step by Step

Use this section if you want to prove the backend works by testing the API directly from the terminal.

### 1. Start the backend

From the project root:

```bash
pipenv install
pipenv shell
cd server
export FLASK_APP=app.py
flask db upgrade
python seed.py
python app.py
```

The API should now be running at `http://127.0.0.1:5555`.

### 2. Test the root route

Open a second terminal and run:

```bash
curl http://127.0.0.1:5555/
```

Expected response:

```json
{
  "message": "Productivity API is running."
}
```

### 3. Confirm protected routes are blocked before login

Run:

```bash
curl -i http://127.0.0.1:5555/notes
```

Expected result:

- Status code: `401 Unauthorized`
- JSON error response showing login is required

### 4. Log in with a seeded demo user

Use one of the demo accounts created by `python seed.py`.

- Username: `alexdev`
- Password: `password123`

Run:

```bash
curl -i -c cookies.txt -X POST http://127.0.0.1:5555/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alexdev","password":"password123"}'
```

What this does:

- `-c cookies.txt` saves the session cookie after login
- The session cookie is what keeps the user authenticated for later requests

Expected result:

- Status code: `200 OK`
- A JSON response with the logged-in user's details

### 5. Check the active session

Run:

```bash
curl -b cookies.txt http://127.0.0.1:5555/check_session
```

What this does:

- `-b cookies.txt` sends the saved session cookie back to the server

Expected result:

- Status code: `200 OK`
- The currently logged-in user is returned

### 6. Fetch the logged-in user's notes

Run:

```bash
curl -b cookies.txt http://127.0.0.1:5555/notes
```

Expected result:

- Status code: `200 OK`
- A paginated JSON response
- Only notes belonging to the logged-in user

You can also test pagination:

```bash
curl -b cookies.txt "http://127.0.0.1:5555/notes?page=1&per_page=2"
```

### 7. Create a new note

Run:

```bash
curl -i -b cookies.txt -X POST http://127.0.0.1:5555/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Proof note","content":"Testing the API from curl.","category":"demo"}'
```

Expected result:

- Status code: `201 Created`
- JSON for the new note, including its `id`

### 8. Get a single note by ID

Use the `id` returned from the create request above. Example:

```bash
curl -b cookies.txt http://127.0.0.1:5555/notes/1
```

Expected result:

- Status code: `200 OK` if the note belongs to the logged-in user
- Status code: `404 Not Found` if that note does not belong to the logged-in user or does not exist

### 9. Update a note

Run:

```bash
curl -i -b cookies.txt -X PATCH http://127.0.0.1:5555/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated proof note","category":"updated-demo"}'
```

Expected result:

- Status code: `200 OK`
- JSON showing the updated note

### 10. Delete a note

Run:

```bash
curl -i -b cookies.txt -X DELETE http://127.0.0.1:5555/notes/1
```

Expected result:

- Status code: `200 OK`
- Empty JSON response

### 11. Log out

Run:

```bash
curl -i -b cookies.txt -X DELETE http://127.0.0.1:5555/logout
```

Expected result:

- Status code: `200 OK`
- Session cleared

### 12. Prove access is removed after logout

Run:

```bash
curl -i -b cookies.txt http://127.0.0.1:5555/check_session
curl -i -b cookies.txt http://127.0.0.1:5555/notes
```

Expected result:

- `GET /check_session` returns `401`
- `GET /notes` returns `401`

### 13. What to show when proving the app works

If you are demonstrating this app to someone, the simplest proof is:

1. Show the root route responds.
2. Show `/notes` fails before login.
3. Log in successfully.
4. Show `/check_session` returns the user.
5. Show `/notes` now works.
6. Create a note.
7. Update or delete that note.
8. Log out.
9. Show `/notes` fails again after logout.
