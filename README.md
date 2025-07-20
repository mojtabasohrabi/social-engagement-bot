# mojtaba sohrabi: This document is written by AI!

# Social Network Engagement Bot

Ever wondered when your favorite influencer hits a milestone? Or maybe you're tracking your own social media growth? This bot's got you covered! It's a Python-based service that keeps an eye on social media profiles, tracks follower changes, and gives you a heads-up when those sweet milestone numbers are reached.

Think of it as your personal social media analytics assistant that never sleeps – checking profiles every 5 minutes and storing all that juicy data for you to analyze later.

## What Can It Do?

Here's what makes this bot special:

- **Multi-Profile Tracking**: Keep tabs on as many Twitter and Instagram profiles as you want – whether it's your own accounts or your favorite creators
- **Auto-Pilot Mode**: Once set up, it checks follower counts every 5 minutes without you lifting a finger
- **Smart Milestone Alerts**: Hit 1K followers? 10K? 1M? Set any milestone you want and get notified when you cross it
- **Growth Analytics**: See how profiles are performing with detailed follower history and daily change tracking
- **Secure & Private**: Each user only sees their own tracked profiles with proper authentication
- **Developer-Friendly**: Comes with a mock social media API so you can test everything without real accounts
- **Background Magic**: All the heavy lifting happens in the background using Celery, so the API stays lightning fast

## The Tech Behind the Magic

We've picked some of the best tools in the Python ecosystem to make this bot reliable and scalable:

- **FastAPI**: The speed demon of Python web frameworks – gives us automatic API docs and blazing performance
- **PostgreSQL**: Rock-solid database that stores all your profiles, follower history, and alerts
- **Redis**: The messenger that helps our background tasks communicate (think of it as the bot's nervous system)
- **Celery**: The workhorse that runs follower checks in the background while keeping the API responsive
- **Docker**: Wraps everything in neat containers so you can run it anywhere without dependency headaches
- **SQLAlchemy**: Makes database operations feel like writing regular Python code

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.13+ (for local development)

### Running with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd social-engagement-bot
```

2. Copy the environment example file:
```bash
cp .env.example .env
```

3. (Optional) Add your Telegram bot token to `.env` for real notifications

4. Start all services:
```bash
docker-compose up -d
```

5. Run database migrations:
```bash
docker-compose exec web alembic upgrade head
```

6. Access the API documentation at http://localhost:8000/docs

## API Endpoints

### Authentication
All endpoints (except user registration) require HTTP Basic Authentication.

### User Management

#### Register User
```bash
POST /api/v1/users/register
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

### Profile Management

#### Create Profile
```bash
POST /api/v1/profiles/
Authorization: Basic <base64_credentials>
Content-Type: application/json

{
  "platform": "twitter",
  "username": "profile_handle"
}
```

#### List Profiles
```bash
GET /api/v1/profiles/
Authorization: Basic <base64_credentials>
```

#### Get Profile Details
```bash
GET /api/v1/profiles/{profile_id}
Authorization: Basic <base64_credentials>
```

#### Get Profile Insights
```bash
GET /api/v1/profiles/{profile_id}/insights
Authorization: Basic <base64_credentials>
```

Returns follower count changes and recent history.

#### Update Profile
```bash
PUT /api/v1/profiles/{profile_id}
Authorization: Basic <base64_credentials>
Content-Type: application/json

{
  "username": "new_handle"
}
```

#### Delete Profile
```bash
DELETE /api/v1/profiles/{profile_id}
Authorization: Basic <base64_credentials>
```

### Alert Management

#### Create Alert
```bash
POST /api/v1/alerts/
Authorization: Basic <base64_credentials>
Content-Type: application/json

{
  "profile_id": 1,
  "threshold": 1000
}
```

#### List Alerts
```bash
GET /api/v1/alerts/
Authorization: Basic <base64_credentials>
```

#### Get Alert Details
```bash
GET /api/v1/alerts/{alert_id}
Authorization: Basic <base64_credentials>
```

#### Update Alert
```bash
PUT /api/v1/alerts/{alert_id}
Authorization: Basic <base64_credentials>
Content-Type: application/json

{
  "threshold": 5000,
  "is_active": true
}
```

#### Delete Alert
```bash
DELETE /api/v1/alerts/{alert_id}
Authorization: Basic <base64_credentials>
```

## Example Workflow

1. **Register a user**:
```bash
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret123"}'
```

2. **Add a profile to monitor**:
```bash
curl -X POST http://localhost:8000/api/v1/profiles/ \
  -u john:secret123 \
  -H "Content-Type: application/json" \
  -d '{"platform": "twitter", "username": "johndoe"}'
```

3. **Set a milestone alert**:
```bash
curl -X POST http://localhost:8000/api/v1/alerts/ \
  -u john:secret123 \
  -H "Content-Type: application/json" \
  -d '{"profile_id": 1, "threshold": 1000}'
```

4. The service will automatically check the profile's follower count every 5 minutes and trigger alerts when milestones are reached.

## Development

### Local Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest
```

### Project Structure

Here's how we've organized the codebase (spoiler: it's pretty intuitive!):

```
social-engagement-bot/
├── app/                  # The heart of our application
│   ├── api/              # REST API endpoints - where HTTP requests come to party
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── users.py     # User registration & login magic
│   │           ├── profiles.py  # CRUD operations for social profiles
│   │           └── alerts.py    # Milestone alert management
│   ├── core/             # Core settings and security stuff
│   │   ├── config.py     # All environment variables live here
│   │   └── security.py   # Password hashing and auth helpers
│   ├── db/               # Database connection setup
│   ├── models/           # Database table definitions (SQLAlchemy style)
│   │   └── profile.py    # User, Profile, FollowerHistory, Alert models
│   ├── schemas/          # Pydantic models for request/response validation
│   ├── services/         # Business logic and external integrations
│   │   ├── mock_social_api.py   # Simulates Twitter/Instagram APIs
│   │   └── telegram_service.py  # Sends notifications (if configured)
│   ├── tasks/            # Background jobs that run on schedule
│   │   ├── celery_app.py        # Celery configuration
│   │   └── follower_tasks.py    # The actual follower checking logic
│   └── tests/            # Making sure everything works as expected
├── alembic/              # Database migration files (not used yet, but ready!)
├── docker-compose.yml    # Orchestrates all our services
├── Dockerfile           # Builds our app container
└── requirements.txt     # All the Python packages we need
```

## How It All Works Together

Let me walk you through what happens under the hood – it's actually pretty cool!

### The Big Picture

Imagine the bot as a well-oiled machine with several moving parts:

1. **The API Server (FastAPI)**: This is the front door. When you make requests to track profiles or set alerts, FastAPI handles them with style. It validates your data, checks your credentials, and talks to the database.

2. **The Database (PostgreSQL)**: Think of this as the bot's memory. It remembers:
   - Who you are (User table)
   - Which profiles you're tracking (Profile table)
   - Every follower count it's ever seen (FollowerHistory table)
   - What milestones you care about (Alert table)

3. **The Background Workers (Celery)**: These are the tireless workers that:
   - Wake up every 5 minutes (thanks to Celery Beat)
   - Check each profile's current follower count
   - Save the data and check if any milestones were hit
   - All while your API stays fast and responsive

4. **The Message Queue (Redis)**: The communication highway between your API and background workers. When it's time to check followers, Redis makes sure the message gets delivered.

### A Day in the Life of a Follower Check

Here's what happens every 5 minutes:

```
1. Celery Beat: "Hey workers, time to check all profiles!"
2. Worker: "On it! Let me grab the list of profiles from the database"
3. Worker → Mock API: "What's @cooluser's follower count?"
4. Mock API: "They have 1,052 followers now"
5. Worker: "Nice! Let me save this to the database"
6. Worker: "Wait... they just crossed 1,000! They had an alert for that!"
7. Worker: "Logging the milestone achievement ✨"
```

### The Data Flow

When you create a new profile to track:
```
Your Request → FastAPI → Validates Data → Saves to PostgreSQL → Returns Success
                                              ↓
                                    Background Worker Picks It Up
                                              ↓
                                    Starts Checking Every 5 Minutes
```

### Why This Architecture?

We chose this setup because:
- **FastAPI** keeps the API super fast and gives you free interactive docs
- **Celery** handles background tasks without slowing down your API calls
- **PostgreSQL** reliably stores all your data with ACID guarantees
- **Redis** ensures messages between services never get lost
- **Docker** makes it work the same on your laptop and in production

## Monitoring & Debugging

Want to see what's happening behind the scenes? We've got you covered:

- **Flower Dashboard** (http://localhost:5555): Watch your background tasks in real-time. See which profiles are being checked, how long it takes, and if anything goes wrong.
- **Interactive API Docs** (http://localhost:8000/docs): Swagger UI lets you test every endpoint right from your browser. No Postman needed!
- **Alternative API Docs** (http://localhost:8000/redoc): Prefer ReDoc? We've got that too.

## Testing

Run the test suite:
```bash
docker-compose exec web pytest
```

Or with coverage:
```bash
docker-compose exec web pytest --cov=app
```
