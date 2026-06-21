# rishi-portfolio

Personal portfolio site. Flask + SQLite on the backend, vanilla JS on the front
with a canvas animation that draws signal pulses crawling along PCB traces.

All the content (profile, skills, projects, experience) lives in the database
and gets served over a small REST API. The HTML is just an empty shell that
hydrates itself on load. The contact form actually works: messages get stored
in the `messages` table.

## running it

```bash
pip install flask
python seed_data.py   # creates portfolio.db and loads resume content
python app.py         # http://localhost:5000
```

## api

| endpoint          | method | what it does                       |
|-------------------|--------|------------------------------------|
| `/api/profile`    | GET    | name, tagline, about, education    |
| `/api/skills`     | GET    | skill groups                       |
| `/api/projects`   | GET    | projects, ordered                  |
| `/api/experience` | GET    | internship + leadership entries    |
| `/api/contact`    | POST   | `{name, email, message}` → sqlite  |
| `/api/ping`       | GET    | health check                       |

## structure

```
app.py            flask routes + api
database.py       sqlite connection / schema
seed_data.py      resume content -> db
templates/        index.html (shell, hydrated by js)
static/js/        circuit_bg.js (canvas), main.js (rendering)
static/css/       style.css
static/img/       photos
```

Updating content = edit `seed_data.py`, rerun it, refresh. Messages survive reseeds.
