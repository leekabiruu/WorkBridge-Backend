# TODO: Implement JWT Authentication and Role-Based Access Control

- [x] Update requirements.txt: Add Flask-JWT-Extended and bcrypt for JWT handling and password hashing.
- [x] Update models.py: Add User model with username, password_hash, and role fields.
- [x] Update app.py: Initialize JWT in app config, add demo users during DB seeding, ensure User table creation.
- [x] Update routes.py: Add /register and /login routes for user creation and JWT issuance; replace header-based role checks with JWT decorators; protect job routes accordingly.
- [x] Install new dependencies: Run `pip install -r requirements.txt`.
- [x] Test the implementation: Run the app, register a user, login to get JWT, test protected routes.
