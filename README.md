---

# JobViper – Job Hunt Tracker CLI

JobViper is a Python console application designed to help users (me) track the progress of their job hunt. 

---

## 🐍 Purpose

* Track all job applications with key details.
* Record interactions with recruiters, hiring managers, and other contacts.
* Monitor outcomes (interview stages, offers, rejections).
* Provide a clear, chronological view of the job search.
* Generate basic stats and dashboards to measure progress.

---

## 🎯 Core Features

### 1. Applications

* Store each job as a unique entity.
* Track:

  * Company name
  * Job title
  * Date applied
  * Source (website, referral, recruiter, etc.)
  * Current status (`applied`, `interview`, `offer`, `rejected`, etc.)
* Assign a unique job ID (e.g., `JV-0001`) automatically.

### 2. Contacts

* Track any interaction related to a job.
* Store for each contact:

  * Date
  * Type (`email`, `phone`, `LinkedIn`, `interview`, `follow-up`)
  * Person / organization
  * Notes

### 3. Results / Outcomes

* Record outcomes or milestones:

  * Status updates (`interview`, `offer`, `rejected`, etc.)
  * Notes (e.g., feedback from recruiter, reason for rejection)
* Automatically update job status based on outcome entries.

### 4. CLI Commands

The command structure is intuitive and extendable:

**Syntax:**

```
jobviper <command> [subcommand] [options]
```

**Examples:**

* Add a job:
  `jobviper add job --company "JetBrains" --title "Senior .NET Developer" --date 2025-12-19`

* List jobs:
  `jobviper list jobs`

* Show job details:
  `jobviper show job JV-0001`

* Add a contact to a job:
  `jobviper contact add JV-0001 --type email --with "Alex P." --notes "Initial outreach"`

* Record a result:
  `jobviper result add JV-0001 --status interview --date 2025-12-28 --notes "Passed recruiter screen"`

### 5. Searching & Filtering (Future)

* Search jobs by company, status, or contact type.
* Filter jobs by date range, stage, or source.

### 6. Dashboard / Stats (Future)

* Quick overview of:

  * Total applications
  * Interviews
  * Offers
  * Rejections
  * Ghosted / no response

### 7. Timeline View (Future)

* Chronological list of all interactions and milestones for a specific job.

---

## 🗂 Data Model

### jobs

| Column       | Type | Description                  |
| ------------ | ---- | ---------------------------- |
| id           | INT  | Auto-incremented primary key |
| company      | TEXT | Company name                 |
| title        | TEXT | Job title                    |
| applied_date | TEXT | Date applied (YYYY-MM-DD)    |
| status       | TEXT | Current status               |
| source       | TEXT | Application source           |

### contacts

| Column | Type | Description              |
| ------ | ---- | ------------------------ |
| job_id | INT  | Foreign key to `jobs.id` |
| date   | TEXT | Date of contact          |
| type   | TEXT | Contact type             |
| person | TEXT | Person contacted         |
| notes  | TEXT | Notes about the contact  |

### results

| Column | Type | Description                            |
| ------ | ---- | -------------------------------------- |
| job_id | INT  | Foreign key to `jobs.id`               |
| date   | TEXT | Date of result                         |
| status | TEXT | Result status (interview, offer, etc.) |
| notes  | TEXT | Notes / feedback                       |

---

## ⚡ Design Philosophy

* Commands read like sentences for fast, intuitive use.
* Fast-path commands for quick daily updates.
* Clear separation of jobs, contacts, and results.
* Easy to extend with dashboards, stats, and follow-up reminders.
* Lightweight, console-first, but expandable with rich output.

---

## 📦 Technical Stack

* Python 3.10+
* CLI: [Typer](https://typer.tiangolo.com/)
* Rich terminal output: [Rich](https://rich.readthedocs.io/)
* Data storage: SQLite (local, lightweight)
* Package management: `pyproject.toml` with editable install for development

---
