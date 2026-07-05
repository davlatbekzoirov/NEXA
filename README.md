# NEXA

NEXA is a Django web app for tracking university applications end to end — deadlines, tasks, scholarships, documents, and test scores — in one place.

## Features

**Application tracking**
- Add universities with type (reach / match / safety), status (preparing, submitted, interview, accepted, rejected, deferred), and deadline
- Auto-generated application checklists (tasks) per university, tailored to the university type
- Regenerate checklists at any time without losing custom or in-progress tasks
- Dashboard with at-a-glance stats: total applications, submitted, accepted, interviews, deadlines due in the next 30 days, and reach/match/safety breakdown
- Deadline timeline and status-distribution data for charting

**Scholarships**
- Track scholarships per university, including amount and currency (USD, EUR, GBP)
- Automatic conversion to USD for applied vs. awarded totals

**Documents**
- Upload and manage application documents
- Version history per document (upload new versions, delete old ones)
- Generate expiring, shareable links to a document for others to view without an account
- Access counter on share links, plus manual revocation

**Test scores**
- Store SAT and IELTS scores, used to help estimate admission chances on "match" schools

**Calendar sync**
- Personal, token-protected iCal feed of application deadlines, subscribable from any calendar app
- Regenerate the feed token to invalidate the old URL

**Accounts**
- Registration, login/logout
- Profile editing, including a profile photo
- Email address changes via a verification-code confirmation step
- Password change

## Tech stack

- **Backend:** Django
- **Async / background tasks:** Celery (see `core/celery.py`, `universities/tasks.py`)
- **Database:** SQLite by default (`db.sqlite3`), swappable via Django settings
- **Templates:** Django templates (`templates/`), no frontend framework required

## Project structure

```
core/            Project settings, URLs, WSGI/ASGI, Celery config
accounts/        Authentication, profile, email change, password change
home/            Marketing/static pages (about, features, help, contact, landing)
universities/    Core domain: universities, scholarships, documents, test scores,
                 application tasks, calendar feed
templates/       HTML templates, organized by app
static/          Static assets (favicon, etc.)
```

## Getting started

### Prerequisites
- Python 3.10+
- pip
- (optional) Redis or another Celery broker, if you want background tasks running

### Setup

```bash
# clone the repo
git clone <your-repo-url>
cd NEXA

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# apply database migrations
python manage.py migrate

# create an admin user
python manage.py createsuperuser

# run the development server
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/`.

### Running Celery (optional)

If you're using the background task features:

```bash
celery -A core worker -l info
```

Make sure your broker (e.g. Redis) is running and configured in `core/settings.py`.

## Calendar feed

Each user gets a private, token-based iCal URL from **Calendar → Subscribe**, in the form:

```
/calendar/<token>.ics
```

This can be added to Google Calendar, Apple Calendar, Outlook, etc. as a subscribed calendar. The token can be regenerated at any time to revoke the old link.

## Document sharing

From a document's detail page, you can generate a time-limited link (1–30 days) that lets anyone with the URL view the document without logging in. Links can be revoked manually and track how many times they've been accessed.

## License

Add your license of choice here.
