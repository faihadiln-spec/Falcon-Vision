# Falcon Vision Project Context For Team Members And AI Agents

## 1. Purpose Of This Document

This document is a detailed handoff for humans and AI coding agents working on Falcon Vision.

Use it when:

- A teammate needs to understand the backend and frontend direction.
- An AI agent needs enough context to safely continue implementation.
- Someone needs to know what has already been built and what should come next.

This is not a marketing document. It is an engineering context document.

---

## 2. Project Overview

Falcon Vision is an AI-powered industrial safety monitoring platform.

The system is designed for factories, industrial facilities, and safety teams. Organizations upload safety regulation PDFs, the backend stores those files, and an LLM-based rule extraction pipeline later converts the text into structured safety rules. Computer vision modules then monitor factory cameras for PPE violations, fall incidents, fire/smoke, hazardous conditions, and face-based access control. Admins and safety supervisors use the web app to manage regulations, employees, face images, permissions, monitoring sessions, detections, alerts, and notifications.

The project currently has two separate local folders:

```text
C:\Users\j4mai\source\repos\FalconVision
C:\Users\j4mai\source\repos\Falcon Vision Web App UI (1)
```

The first folder is the backend.

The second folder is the frontend.

---

## 3. Current Technology Stack

### Backend

```text
FastAPI
MongoDB Atlas
Motor
PyMongo
Pydantic v2
JWT auth
Passlib + bcrypt
python-jose
```

The backend is async-first and uses Motor for MongoDB access.

### Frontend

```text
React
Vite
TypeScript
React Router
React Hook Form
Zod
Sonner toast notifications
Tailwind / custom CSS
```

The frontend currently has pages generated from a UI design and is being gradually connected to the backend.

---

## 4. High-Level Architecture

The backend follows a clean architecture style without becoming an overengineered microservice system.

The main rule is:

```text
Routes handle HTTP.
Schemas validate request/response payloads.
Services contain business logic.
Repositories talk to MongoDB.
Models define MongoDB document shapes.
Integrations isolate external systems like AI, storage, and notifications.
Core contains config, database, security, permissions, constants, and exceptions.
```

Do not put database calls directly in route files.

Do not put HTTP-specific behavior inside repositories.

Do not put AI vendor code inside business services.

---

## 5. Backend Folder Structure

Backend root:

```text
C:\Users\j4mai\source\repos\FalconVision\backend
```

Current structure:

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── auth_routes.py
│   │       ├── user_routes.py
│   │       ├── regulation_routes.py
│   │       ├── extraction_job_routes.py
│   │       ├── employee_face_routes.py
│   │       ├── monitoring_session_routes.py
│   │       ├── alert_routes.py
│   │       └── health_routes.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── permissions.py
│   │   ├── exceptions.py
│   │   └── constants.py
│   ├── models/
│   │   ├── base.py
│   │   ├── organization_model.py
│   │   ├── user_model.py
│   │   ├── regulation_model.py
│   │   ├── extracted_rule_model.py
│   │   ├── extraction_job_model.py
│   │   ├── employee_model.py
│   │   ├── employee_face_model.py
│   │   ├── zone_model.py
│   │   ├── employee_zone_permission_model.py
│   │   ├── camera_model.py
│   │   ├── monitoring_session_model.py
│   │   ├── detection_model.py
│   │   ├── alert_model.py
│   │   ├── notification_model.py
│   │   └── audit_log_model.py
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── common_schema.py
│   │   └── placeholder schema files for future modules
│   ├── repositories/
│   │   ├── base_repository.py
│   │   ├── organization_repository.py
│   │   ├── user_repository.py
│   │   └── placeholder repository files for future modules
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── placeholder service files for future modules
│   ├── integrations/
│   │   ├── ai/
│   │   ├── storage/
│   │   └── notifications/
│   ├── jobs/
│   └── utils/
├── scripts/
│   ├── check_mongo_connection.py
│   └── create_indexes.py
├── postman/
│   └── FalconVision.postman_collection.json
├── uploads/
├── requirements.txt
├── README.md
└── .env.example
```

---

## 6. Backend Layers In Detail

### 6.1 `app/main.py`

This creates the FastAPI app.

Current responsibilities:

- Creates the FastAPI instance.
- Connects to MongoDB during lifespan startup.
- Closes MongoDB connection during shutdown.
- Registers CORS for the Vite frontend.
- Registers global app error handling.
- Registers routers.

Current registered routes:

```text
GET  /api/health
POST /api/auth/register-organization
POST /api/auth/login
GET  /api/auth/me
POST /api/users
```

### 6.2 `api/routes`

Routes are thin HTTP adapters.

They should:

- Accept request bodies.
- Use FastAPI dependencies.
- Call service methods.
- Return response schemas.

They should not:

- Query MongoDB directly.
- Hash passwords directly.
- Generate JWTs directly.
- Implement business rules directly.

### 6.3 `api/deps.py`

This file defines FastAPI dependencies.

Current responsibilities:

- Creates repositories from the current MongoDB database.
- Creates services from repositories.
- Defines OAuth2 bearer token extraction.
- Implements `get_current_user`.

Important behavior:

```text
Authorization: Bearer <access_token>
```

is required for protected endpoints.

### 6.4 `core/config.py`

Uses Pydantic Settings.

It loads environment variables from:

```text
.env
../.env
```

This was done because the real `.env` currently exists in the repository root:

```text
C:\Users\j4mai\source\repos\FalconVision\.env
```

while backend commands usually run from:

```text
C:\Users\j4mai\source\repos\FalconVision\backend
```

Important settings:

```text
MONGO_URI
MONGO_DB_NAME
JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
UPLOAD_DIR
MAX_PDF_SIZE_MB
MAX_FACE_IMAGE_SIZE_MB
```

### 6.5 `core/database.py`

Uses Motor:

```text
motor.motor_asyncio.AsyncIOMotorClient
```

Current exported functions:

```text
connect_to_mongo()
close_mongo_connection()
get_database()
```

The Mongo client uses `certifi` for TLS certificate trust when connecting to MongoDB Atlas.

### 6.6 `core/security.py`

Current responsibilities:

- Hash passwords.
- Verify passwords.
- Create JWT access tokens.
- Decode JWT access tokens.

Libraries:

```text
passlib
bcrypt==4.0.1
python-jose
```

Important note:

`bcrypt` is pinned to `4.0.1` because `passlib==1.7.4` has compatibility issues with `bcrypt 5.x`.

Password max length is set to 72 characters because bcrypt only safely supports up to 72 bytes.

### 6.7 `core/constants.py`

Central enum definitions live here.

Examples:

```text
UserRole
UserStatus
OrganizationStatus
RegulationStatus
ExtractionStatus
RuleCategory
Severity
VisionModule
AlertStatus
NotificationStatus
```

AI agents should use these enums instead of inventing random strings.

### 6.8 `core/exceptions.py`

Defines application-level errors:

```text
AppError
NotFoundError
ConflictError
InvalidCredentialsError
PermissionDeniedError
InactiveUserError
```

`app/main.py` converts these errors to JSON HTTP responses.

### 6.9 `models`

Models define MongoDB document shapes.

They are not API request schemas.

Examples:

```text
UserModel
OrganizationModel
RegulationModel
ExtractedRuleModel
EmployeeModel
CameraModel
AlertModel
DetectionModel
```

Important base model:

```text
models/base.py
```

This defines:

```text
PyObjectId
MongoModel
TimestampMixin
SoftDeleteMixin
TenantModel
```

`PyObjectId` keeps MongoDB inserts as real `ObjectId` values while serializing to string for JSON.

### 6.10 `schemas`

Schemas define API request and response payloads.

Currently implemented:

```text
auth_schema.py
user_schema.py
common_schema.py
```

### 6.11 `repositories`

Repositories talk to MongoDB.

Currently implemented:

```text
BaseRepository
OrganizationRepository
UserRepository
```

Repositories should not enforce business permissions.

### 6.12 `services`

Services contain business rules.

Currently implemented:

```text
AuthService
UserService
```

Services coordinate repositories, security helpers, and validation decisions.

---

## 7. MongoDB Atlas Setup

The project uses MongoDB Atlas.

The backend has already connected successfully and created 15 collections.

Connection check script:

```powershell
cd C:\Users\j4mai\source\repos\FalconVision\backend
python scripts/check_mongo_connection.py
```

Expected output:

```text
MongoDB connection: OK
Collections found: 15
```

Index creation script:

```powershell
python scripts/create_indexes.py
```

This creates indexes for:

```text
organizations
users
regulations
extracted_rules
extraction_jobs
employees
employee_faces
zones
employee_zone_permissions
cameras
monitoring_sessions
detections
alerts
notifications
audit_logs
```

---

## 8. MongoDB Collections

### 8.1 `organizations`

Represents a tenant, factory, or company.

Important fields:

```text
name
industry
country
city
address
status
settings
created_at
updated_at
is_deleted
```

### 8.2 `users`

Stores all dashboard users in one collection.

Important design decision:

```text
Use one users collection with role field.
Do not create separate admin/supervisor collections.
```

Roles:

```text
system_admin
organization_admin
safety_supervisor
security_operator
viewer
```

Important fields:

```text
organization_id
full_name
email
password_hash
role
status
last_login_at
profile
permissions_override
created_at
updated_at
created_by
updated_by
is_deleted
```

### 8.3 `regulations`

Stores uploaded regulation PDF metadata.

Actual PDF files should not be stored inside MongoDB.

Store file metadata:

```text
original_filename
storage_provider
storage_path
mime_type
size_bytes
sha256
```

Extraction state:

```text
not_started
pending
processing
completed
failed
```

### 8.4 `extracted_rules`

Stores structured safety rules extracted from PDFs.

This is separate from `regulations` because monitoring modules need to query rules directly.

Example categories:

```text
ppe
fall
fire_smoke
hazard
access_control
general_safety
```

### 8.5 `employees`

Represents real employees, contractors, or visitors monitored by cameras.

Important distinction:

```text
Employees are not the same as users.
```

A factory worker may be monitored by the system without being able to log in.

### 8.6 `employee_faces`

Stores employee face image metadata and embeddings.

Images should be stored in local storage for now:

```text
backend/uploads/employee_faces
```

Later this can move to S3, MinIO, or Azure Blob.

Embeddings currently fit in MongoDB for graduation-project scale.

Later this can move to MongoDB Atlas Vector Search or a dedicated vector database.

### 8.7 `zones`

Represents physical areas:

```text
entrance
production
warehouse
maintenance
restricted
office
emergency_exit
fire_risk
```

Zones are important because cameras, permissions, detections, and alerts are tied to location.

### 8.8 `employee_zone_permissions`

Many-to-many relationship between employees and zones.

This is its own collection because zone permissions have:

```text
permission_type
reason
valid_from
valid_until
status
created_by
updated_by
```

### 8.9 `cameras`

Stores camera stream metadata and enabled vision modules.

Vision modules:

```text
ppe_detection
fall_detection
fire_smoke_detection
hazard_detection
face_access_control
```

### 8.10 `monitoring_sessions`

Represents an active or historical monitoring run.

Sessions group:

```text
cameras
zones
modules
detections
alerts
```

### 8.11 `detections`

Stores raw or semi-processed computer vision events.

Examples:

```text
ppe_violation
fall_detected
fire_detected
smoke_detected
hazard_detected
unauthorized_access
unknown_face_detected
authorized_access
```

Detections can be high-volume, so do not embed them inside sessions or cameras.

### 8.12 `alerts`

Stores actionable safety alerts.

Important distinction:

```text
Not every detection is an alert.
```

Alerts include workflow state:

```text
open
acknowledged
resolved
dismissed
false_positive
```

Alerts also store snapshots of camera, zone, employee, and rule names so historical alerts remain readable even if those records are renamed later.

### 8.13 `notifications`

Tracks messages sent to users.

Channels:

```text
in_app
email
sms
websocket
```

### 8.14 `audit_logs`

Append-only audit trail.

Use for:

```text
login-sensitive events
organization changes
user creation
face uploads
permission changes
alert acknowledgement
alert resolution
```

---

## 9. Current Auth Behavior

### 9.1 Register Organization

Endpoint:

```text
POST /api/auth/register-organization
```

Purpose:

Creates:

```text
organization
first organization_admin user
```

Important behavior:

```text
Registration does not log the user in.
Registration does not return an access token.
```

Request example:

```json
{
  "organization_name": "Falcon Steel Factory",
  "industry": "manufacturing",
  "country": "Saudi Arabia",
  "city": "Riyadh",
  "address": "Industrial Zone 2",
  "admin_full_name": "Admin User",
  "admin_email": "admin@example.com",
  "admin_password": "StrongPass123",
  "admin_phone": "+966500000000"
}
```

Response shape:

```json
{
  "organization": {
    "id": "...",
    "name": "Falcon Steel Factory",
    "status": "active"
  },
  "user": {
    "id": "...",
    "organization_id": "...",
    "full_name": "Admin User",
    "email": "admin@example.com",
    "role": "organization_admin",
    "status": "active"
  }
}
```

### 9.2 Login

Endpoint:

```text
POST /api/auth/login
```

Request:

```json
{
  "email": "admin@example.com",
  "password": "StrongPass123"
}
```

Response:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

The frontend stores this token in localStorage.

### 9.3 Get Current User

Endpoint:

```text
GET /api/auth/me
```

Requires:

```text
Authorization: Bearer <access_token>
```

Returns the authenticated user.

### 9.4 Create User

Endpoint:

```text
POST /api/users
```

Requires admin token.

Only these users can create users:

```text
system_admin
organization_admin
```

Current request:

```json
{
  "full_name": "Safety Viewer",
  "email": "viewer@example.com",
  "password": "StrongPass123",
  "role": "viewer",
  "phone": "+966500000001",
  "job_title": "Safety Viewer"
}
```

Important:

Public signup only creates the first organization admin.

Safety supervisors should be created later by an authenticated admin through `POST /api/users`.

---

## 10. Frontend Integration

Frontend root:

```text
C:\Users\j4mai\source\repos\Falcon Vision Web App UI (1)
```

### 10.1 API Client

File:

```text
src/app/lib/api.ts
```

Current responsibilities:

- Defines backend base URL.
- Sends JSON requests.
- Parses backend error responses.
- Exposes:

```text
registerOrganization()
login()
getMe()
```

Default backend base URL:

```text
http://127.0.0.1:8000
```

Can be overridden with:

```text
VITE_API_BASE_URL
```

### 10.2 Auth Storage

File:

```text
src/app/lib/auth.ts
```

Current localStorage keys:

```text
falcon_vision_access_token
falcon_vision_user
```

Current helpers:

```text
saveAuthSession()
getAccessToken()
getAuthUser()
clearAuthSession()
getHomePathForRole()
```

Role redirect behavior:

```text
organization_admin -> /admin
system_admin       -> /admin
safety_supervisor  -> /supervisor
other roles        -> /supervisor/no-permission
```

### 10.3 Login Page

File:

```text
src/app/pages/LoginPage.tsx
```

Current behavior:

1. User enters email and password.
2. Frontend calls `POST /api/auth/login`.
3. Frontend calls `GET /api/auth/me` with returned token.
4. Frontend stores token and user in localStorage.
5. Frontend redirects based on backend role.

The old fake login delay has been removed.

The old manual "login as admin/supervisor" selector has been removed because role must come from the backend, not from the UI.

### 10.4 Signup Page

File:

```text
src/app/pages/SignUpPage.tsx
```

Current behavior:

1. User enters organization name and admin details.
2. Frontend calls `POST /api/auth/register-organization`.
3. Backend creates organization and first admin user.
4. Backend does not return token.
5. Frontend redirects to login.

Important design decision:

Public signup should not create safety supervisors directly.

The first public account is always the organization admin.

Supervisors and other users should be created later from the admin dashboard.

---

## 11. How To Run Locally

### 11.1 Start Backend

```powershell
cd C:\Users\j4mai\source\repos\FalconVision\backend
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

### 11.2 Start Frontend

```powershell
cd "C:\Users\j4mai\source\repos\Falcon Vision Web App UI (1)"
npm run dev
```

Frontend URL is usually:

```text
http://localhost:5173
```

### 11.3 Test Flow

1. Open frontend.
2. Go to signup.
3. Register a new organization/admin.
4. You should be redirected to login.
5. Log in with the same email and password.
6. Admin should be redirected to `/admin`.

---

## 12. Postman Collection

Postman collection:

```text
C:\Users\j4mai\source\repos\FalconVision\backend\postman\FalconVision.postman_collection.json
```

It includes:

```text
Health Check
Register Organization
Login
Get Me
Create User
```

Important:

The Register Organization request does not save a token.

The Login request saves the token.

Run order:

```text
Health Check
Register Organization
Login
Get Me
Create User
```

---

## 13. Environment Variables

Example file:

```text
backend/.env.example
```

Real local file currently exists at:

```text
C:\Users\j4mai\source\repos\FalconVision\.env
```

Required values:

```env
APP_NAME=Falcon Vision API
ENVIRONMENT=development
DEBUG=true

MONGO_URI=mongodb+srv://...
MONGO_DB_NAME=falcon_vision

JWT_SECRET_KEY=...
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

UPLOAD_DIR=uploads
MAX_PDF_SIZE_MB=25
MAX_FACE_IMAGE_SIZE_MB=10
```

Do not commit real `.env` secrets.

---

## 14. Important Security Notes

### 14.1 JWT Secret

A strong JWT secret was generated locally and placed in `.env`.

If the JWT secret changes, all old tokens become invalid.

### 14.2 Passwords

Passwords are stored as hashes, not plaintext.

Hashing uses:

```text
passlib + bcrypt
```

### 14.3 Roles

Never trust frontend-selected roles for authorization.

The backend role stored in MongoDB is the source of truth.

### 14.4 CORS

Backend currently allows:

```text
http://localhost:5173
http://127.0.0.1:5173
```

This is for local development.

Production should use the real frontend domain.

---

## 15. What Is Implemented Right Now

Implemented:

- Backend folder architecture.
- MongoDB models for the main collections.
- MongoDB Atlas connection.
- Index creation script.
- Connection check script.
- JWT security helpers.
- Organization registration.
- Login.
- Current user endpoint.
- Admin-created users.
- App-level error handling.
- CORS for frontend.
- Postman collection.
- Frontend signup connected to backend.
- Frontend login connected to backend.
- Frontend auth token/user localStorage helpers.

---

## 16. What Is Not Implemented Yet

Not implemented yet:

- Real protected route guards in React.
- Logout button behavior.
- Admin dashboard user management UI connected to `POST /api/users`.
- Listing users.
- Updating users.
- Deactivating users.
- Refresh tokens.
- Forgot password flow.
- Email verification.
- Regulation PDF upload.
- Local file storage implementation for PDFs.
- Rule extraction worker.
- LLM integration.
- Employee CRUD.
- Employee face upload.
- Face embedding generation.
- Zone CRUD.
- Zone permission CRUD.
- Camera CRUD.
- Monitoring sessions.
- Detection ingestion endpoint.
- Alert creation workflow.
- Notification service.
- Audit log writing.
- Tests.

---

## 17. Recommended Next Backend Steps

### Step 1: Add Auth Guards And Role Dependencies

Implement reusable dependencies:

```text
require_roles(...)
require_admin
require_supervisor_or_admin
```

File:

```text
app/core/permissions.py
app/api/deps.py
```

### Step 2: Add User Management

Endpoints:

```text
GET    /api/users
GET    /api/users/{user_id}
PATCH  /api/users/{user_id}
PATCH  /api/users/{user_id}/status
```

### Step 3: Add Organization Profile Endpoint

Endpoints:

```text
GET   /api/organizations/me
PATCH /api/organizations/me
```

### Step 4: Add Regulation Upload

Implement:

```text
StorageClient
LocalStorageClient
RegulationRepository
RegulationService
POST /api/regulations/upload
GET /api/regulations
```

### Step 5: Add Extraction Jobs

Implement:

```text
ExtractionJobRepository
ExtractionJobService
MockRuleExtractionClient
```

Start with mock extraction before real LLM integration.

---

## 18. Recommended Next Frontend Steps

### Step 1: Add Protected Routes

Use localStorage token and `/api/auth/me` to protect:

```text
/admin/*
/supervisor/*
```

### Step 2: Add Logout

Logout should:

```text
clear localStorage
redirect to /login
```

### Step 3: Connect Admin User Creation UI

If there is no page for it yet, add one under admin settings or a dedicated users page.

Call:

```text
POST /api/users
```

### Step 4: Display Current User

Admin and supervisor profile pages should use stored user or call:

```text
GET /api/auth/me
```

---

## 19. Backend Request Flow Example

Example: login.

```text
LoginPage.tsx
  -> POST /api/auth/login
    -> auth_routes.py
      -> AuthService.login()
        -> UserRepository.find_by_email()
          -> MongoDB users collection
        -> verify_password()
        -> create_access_token()
      -> TokenResponse
```

Example: create user.

```text
Frontend admin page
  -> POST /api/users with Bearer token
    -> user_routes.py
      -> get_current_user()
        -> decode JWT
        -> UserRepository.find_by_id()
      -> UserService.create_user()
        -> check current user role
        -> hash password
        -> UserRepository.create()
          -> MongoDB users collection
      -> UserResponse
```

---

## 20. Design Decisions AI Agents Must Preserve

### Preserve One Users Collection

Do not create:

```text
admins
supervisors
operators
```

Use:

```text
users.role
```

### Keep Employees Separate From Users

Dashboard users log in.

Employees are monitored by the safety system.

These are different concepts.

### Keep Regulations Separate From Extracted Rules

`regulations` stores PDF metadata.

`extracted_rules` stores structured AI-extracted rules.

### Keep Detections Separate From Alerts

Detections are raw/semi-processed CV events.

Alerts are actionable workflow items.

### Do Not Mix AI Code Into Routes

AI integrations should go under:

```text
app/integrations/ai
```

Services decide when to call AI.

Integrations decide how to call AI.

Repositories decide where to store data.

### Do Not Store Large Files In MongoDB

Store files locally for now under:

```text
backend/uploads
```

Store only file metadata in MongoDB.

Later use S3, MinIO, Azure Blob, or similar.

---

## 21. Known Current Limitations

### No Refresh Tokens

Only access tokens exist.

For a graduation project this is acceptable initially.

### No Email Verification

Organization registration immediately creates the admin.

### No Database Transactions Yet

Organization registration creates an organization, then creates a user.

In production, this should ideally use a MongoDB transaction so both insertions succeed or both fail.

For now, duplicate checks reduce risk, but this can be improved.

### Frontend Uses localStorage

JWT is stored in localStorage.

This is practical for the current project.

For stronger production security, consider HttpOnly cookies.

---

## 22. Verification Commands

Backend syntax/import check:

```powershell
cd C:\Users\j4mai\source\repos\FalconVision
python -m compileall backend\app backend\scripts
```

Mongo connection check:

```powershell
cd C:\Users\j4mai\source\repos\FalconVision\backend
python scripts/check_mongo_connection.py
```

Frontend build check:

```powershell
cd "C:\Users\j4mai\source\repos\Falcon Vision Web App UI (1)"
npm run build
```

---

## 23. Practical Instructions For AI Agents

When continuing this project:

1. Read this file first.
2. Inspect the specific files you will edit.
3. Keep backend changes inside the clean architecture layers.
4. Do not move frontend folders unless asked.
5. Do not hardcode secrets.
6. Do not print `.env` values.
7. Use existing enums from `core/constants.py`.
8. Add schemas for request/response payloads.
9. Put Mongo queries in repositories.
10. Put business rules in services.
11. Use `get_current_user` for protected backend routes.
12. Use `Authorization: Bearer <token>` from the frontend.
13. Run compile/build checks after changes.

---

## 24. Current Mental Model

Falcon Vision is being built in vertical slices.

Completed first slice:

```text
Organization registration
User login
JWT auth
Frontend auth connection
```

Next slices should follow the same pattern:

```text
schema
model if needed
repository
service
route
frontend API client
frontend page wiring
verification
```

This keeps the project understandable, demoable, and safe to grow.
