# NEXA

NEXA is a Django web app that helps students manage university applications, coursework, extracurricular life, housing, roommate finances, and personal budgeting — all in one place.

## Modules

NEXA is organized into four user-facing modules, each backed by one or more Django apps.

### UniTracker
*(Django app: `universities`)*

- Add universities with type (reach / match / safety), status (preparing, submitted, interview, accepted, rejected, deferred), and deadline
- Auto-generated application checklists (tasks) per university, tailored to the university type
- Regenerate checklists at any time without losing custom or in-progress tasks
- Dashboard with at-a-glance stats: total applications, submitted, accepted, interviews, deadlines due in the next 30 days, and reach/match/safety breakdown
- Deadline timeline and status-distribution data for charting
- University autocomplete when adding a new school

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

### SmartStudy
*(Django app: `smart_study`)*

- Course and category management, with assignments tracked per course
- Grade tracking and analytics on performance over time, including What-If and Target Grade scenarios
- Study scheduler for planning coursework and sessions
- Built-in Pomodoro timer for focused study sessions
- Study groups: create/join groups, group detail pages
- Social features: friends list and activity
- Personal analytics dashboard

### CampusPulse
*(Django app: `extracurricular`)*

- Track clubs, membership, and club details
- Log events and volunteer work
- Record impact entries to quantify contributions over time
- Analytics/insights on extracurricular activity
- Campus-wide activity feed
- Public portfolio page to showcase clubs, events, and volunteer impact, with configurable portfolio settings
- Auto-generated resume content from tracked activities

### CampusCribs
*(Django apps: `housing`, `roomieratio`, `budget`)*

**Housing**
- Track student housing/dorm search as a pipeline, from shortlisting through application and move-in
- Dedicated pipeline view (`housing/pipeline.html`) for managing housing options alongside university applications

**RoomieRatio**
- Manage shared households with roommates and split costs fairly
- Central hub view for an active household (`roomieratio/hub.html`)
- Fallback/onboarding view when a user isn't part of a household yet (`roomieratio/no_household.html`)
- Shared helper logic for ratio/split calculations (`roomieratio/utils.py`)

**Budget**
- Personal budget dashboard for tracking finances alongside applications and school costs

### Accounts
*(Django app: `accounts`)*

- Registration, login/logout
- Profile editing, including a profile photo
- Email address changes via a verification-code confirmation step
- Password change

## Design & UI

The public-facing pages (`home/`, i.e. landing, about, features, help, contact) share a single visual system built in `templates/base/base.html`, using no frontend framework or build step — just CSS custom properties and vanilla JS.

**Theme:** a dark, "ledger and brass" aesthetic — deep green surfaces, cream ink-colored type, brass accents, dashed stamp-style borders, and Fraunces/IBM Plex Sans/Mono for type — meant to feel like a well-kept record book rather than a generic SaaS dashboard.

**Interactive touches, all progressively enhanced and safe under `prefers-reduced-motion`:**
- **Scroll-reveal** — sections and cards fade/slide into place as they enter the viewport (`data-reveal`, with optional `data-reveal-delay` for staggering groups), via a small shared `IntersectionObserver`
- **Spotlight hover cards** — a soft glow that follows the cursor across feature/module cards (`.spotlight-card`)
- **Ambient background** — a lightweight, dependency-free canvas with slow-drifting brass/green/blue gradient blobs behind the nav and page content
- **Count-up stats** — numeric stat values animate from 0 up to their target the first time they're scrolled into view (`data-count-to="N"` on a `.stat-value`)
- **Testimonial marquee** — an infinite, seamless-looping row of student comments on the homepage that pauses on hover (currently placeholder quotes — swap in real feedback before launch)
- **Animated FAQ accordion** — the Help page's native `<details>`/`<summary>` list smoothly animates open/closed height via the Web Animations API instead of snapping, while keeping native keyboard accessibility
- **Micro-interactions** — animated nav underlines, a spinning brand mark on hover, a diagonal shine sweep on buttons, and a "sending…" spinner state on the contact form's submit button
- **Site footer** — brass "ledger stamp" detail, mono-styled link columns anchored to each module's section on the About page, and a dashed badge pill in the footer bottom bar

All of this lives in plain CSS/JS inside `base.html` and each page template, so no npm install or bundler is required to run or extend it.

## Tech stack

- **Backend:** Django
- **Async / background tasks:** Celery (see `core/celery.py`, `universities/tasks.py`, `extracurricular/tasks.py`)
- **Database:** SQLite by default (`db.sqlite3`), swappable via Django settings
- **Templates:** Django templates (`templates/`), no frontend framework required
- **Frontend interactivity:** vanilla CSS/JS — CSS custom properties for theming, `IntersectionObserver` for scroll-reveal and count-up animations, and the Web Animations API for the FAQ accordion; no build step, bundler, or JS framework

## Project structure

```
core/              Project settings, URLs, WSGI/ASGI, Celery config
accounts/          Authentication, profile, email change, password change
home/              Marketing/static pages (about, features, help, contact, landing)
universities/      UniTracker — application tracking: universities, scholarships,
                   documents, test scores, application tasks, calendar feed
smart_study/       SmartStudy — courses, assignments, grades, scheduler, study
                   groups, friends/social, Pomodoro timer, analytics
extracurricular/   CampusPulse — clubs, events, volunteering, impact tracking,
                   public portfolio, resume generator, campus feed
housing/           CampusCribs — student housing/dorm pipeline tracking
roomieratio/       CampusCribs — shared household management and cost/ratio
                   splitting between roommates
budget/            CampusCribs — personal budget dashboard
templates/         HTML templates, organized by app
static/            Static assets (favicon, etc.)
media/             User-uploaded files (e.g. profile photos)
```

## Getting started

### Prerequisites
- Python 3.10+
- pip
- (optional) Redis or another Celery broker, if you want background tasks running

### Setup

```bash
# clone the repo
git clone https://github.com/davlatbekzoirov/NEXA.git
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

cp .env.dist .env
```

Then visit `http://127.0.0.1:8000/`.

### Running Celery (optional)

If you're using the background task features:

```bash
celery -A core worker -l info
```

Make sure your broker (e.g. Redis) is running and configured in `core/settings.py`.

## Calendar feed

Each user gets a private, token-based iCal URL from **UniTracker → Calendar → Subscribe**, in the form:

```
/calendar/<token>.ics
```

This can be added to Google Calendar, Apple Calendar, Outlook, etc. as a subscribed calendar. The token can be regenerated at any time to revoke the old link.

## Document sharing

From a document's detail page in **UniTracker**, you can generate a time-limited link (1–30 days) that lets anyone with the URL view the document without logging in. Links can be revoked manually and track how many times they've been accessed.

## Public portfolio

**CampusPulse** activity (clubs, events, volunteer work, and impact) can be published to a public, shareable portfolio page, with settings to control what's visible.

## RoomieRatio

Part of **CampusCribs**, RoomieRatio helps students living with roommates track shared expenses and split costs by a configurable ratio. New users without a household see an onboarding prompt; once part of a household, the hub view becomes the central place to manage shared costs.

## License

Add your license of choice here.