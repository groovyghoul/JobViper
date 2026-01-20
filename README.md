---

# JobViper – Job Hunt Tracker CLI

JobViper is a Python console application designed to help users (me) track the progress of their job hunt. 

---

## Purpose

* Track all job applications with key details.
* Record interactions with recruiters, hiring managers, and other contacts.
* Monitor outcomes (interview stages, offers, rejections).
* Provide a clear, chronological view of the job search.
* Generate basic stats and dashboards to measure progress.

---

## Core Features

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

### 4. CLI Command Reference

(NOTE: the command structure is still a WIP...this may (will) change soon)

The command structure is intuitive and extendable:

**Syntax:**

```
jobviper <command> [subcommand] [options]
```

Use these commands to manage your job search workflow. All commands support the `--help` flag for detailed information.

### Table of Contents

* `jobviper add-job` - Create a new application.
* `jobviper list-jobs` - View all applications.
* `jobviper show-job` - View detailed info for a specific job.
* `jobviper contact add` - Track networking and follow-ups.
* `jobviper result add` - Record application outcomes.

---

### `jobviper add-job`

Adds a new job application to your tracker.

#### **Usage**

```bash
jobviper add-job [OPTIONS]

```

#### **Options**

| Option | Shorthand | Type | Description |
| --- | --- | --- | --- |
| `--company` | `-c` | **TEXT** | **Required.** Name of the company. |
| `--title` | `-t` | **TEXT** | **Required.** Job title (e.g., Software Engineer). |
| `--date` | `-d` | **DATE** | Date of application (defaults to current if omitted). |
| `--source` | `-s` | **TEXT** | Where you found the job (e.g., LinkedIn, Indeed). |

---

### `jobviper list-jobs`

Displays a list of all your recorded job applications.

#### **Usage**

```bash
jobviper list-jobs

```

---

### `jobviper show-job`

Shows comprehensive details for a specific job application, including associated contacts and results.

#### **Usage**

```bash
jobviper show-job JOB_ID

```

#### **Arguments**

* **`JOB_ID`** (TEXT, Required): The unique identifier for the job (e.g., `JV-0001`).

---

### `jobviper contact add`

Adds a new contact entry for a specific job application to track networking.

#### **Usage**

```bash
jobviper contact add [OPTIONS] JOB_ID

```

#### **Arguments**

* **`JOB_ID`** (TEXT, Required): The unique identifier for the job.

#### **Options**

| Option | Shorthand | Type | Description |
| --- | --- | --- | --- |
| `--type` | `-t` | **TEXT** | **Required.** Type of contact (e.g., email, LinkedIn). |
| `--with` | `-w` | **TEXT** | **Required.** Person or organization contacted. |
| `--notes` | `-n` | **TEXT** | Additional notes about the interaction. |
| `--date` | `-d` | **DATE** | Date of contact. |

---

### `jobviper result add`

Records a new result or outcome for a job application and automatically updates the job status.

#### **Usage**

```bash
jobviper result add [OPTIONS] JOB_ID

```

#### **Arguments**

* **`JOB_ID`** (TEXT, Required): The unique identifier for the job.

#### **Options**

| Option | Shorthand | Type | Description |
| --- | --- | --- | --- |
| `--status` | `-s` | **TEXT** | **Required.** Status update (e.g., interview, offer, rejected). |
| `--date` | `-d` | **DATE** | Date of the result. |
| `--notes` | `-n` | **TEXT** | Notes about the outcome. |

---

### Supported Date Formats

For any command accepting a `--date` flag, the following formats are valid:

* `YYYY-MM-DD` (e.g., 2026-01-19)
* `YYYY-MM-DDTHH:MM:SS`
* `YYYY-MM-DD HH:MM:SS`

---

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

## Data Model

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

## To hack on JobViper

```bash
git clone <https://github.com/groovyghoul/JobViper.git>

cd JobViper
python -m venv venv
source venv/bin/activate
pip install -e .
```

---

## Technical Stack

* Python 3.10+
* CLI: [Typer](https://typer.tiangolo.com/)
* Rich terminal output: [Rich](https://rich.readthedocs.io/)
* Data storage: SQLite (local, lightweight)
* Package management: `pyproject.toml` with editable install for development

---
