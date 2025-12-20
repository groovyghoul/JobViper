import typer
from rich.console import Console
from rich.table import Table
from jobviper.database import engine
from jobviper.models import Base, Job, Contact, Result
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date

app = typer.Typer()
console = Console()

@app.command()
def initdb():
    """
    Initializes the database.
    """
    Base.metadata.create_all(bind=engine)
    console.print("[bold green]Database initialized.[/bold green]")

@app.command()
def add_job(
    company: str = typer.Option(..., "--company", "-c"),
    title: str = typer.Option(..., "--title", "-t"),
    date: datetime = typer.Option(None, "--date", "-d"),
    source: str = typer.Option(None, "--source", "-s"),
):
    """
    Adds a new job application.
    """
    if date is None:
        date = datetime.now()

    db_session = sessionmaker(bind=engine)
    db = db_session()
    
    job = Job(
        company=company,
        title=title,
        applied_date=date.date(),
        source=source,
        status="applied",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    db.close()
    
    console.print(f"[bold green]Added job application for {title} at {company}.[/bold green]")

@app.command()
def list_jobs():
    """
    Lists all job applications.
    """
    db_session = sessionmaker(bind=engine)
    db = db_session()
    
    jobs = db.query(Job).all()
    db.close()

    table = Table("ID", "Company", "Title", "Applied Date", "Status", "Source")
    for job in jobs:
        table.add_row(
            f"JV-{job.id:04}",
            job.company,
            job.title,
            str(job.applied_date),
            job.status,
            job.source,
        )
    
    console.print(table)


contact_app = typer.Typer()
app.add_typer(contact_app, name="contact", help="Manage job contacts.")

@contact_app.command("add")
def add_contact(
    job_id: str = typer.Argument(..., help="Job ID (e.g., JV-0001)"),
    type: str = typer.Option(..., "--type", "-t", help="Type of contact (e.g., email, phone, LinkedIn)"),
    person: str = typer.Option(..., "--with", "-w", help="Person or organization contacted"),
    notes: str = typer.Option(None, "--notes", "-n", help="Notes about the contact"),
    contact_date: datetime = typer.Option(None, "--date", "-d", help="Date of contact (YYYY-MM-DD)"),
):
    """
    Adds a new contact for a job application.
    """
    if contact_date is None:
        contact_date = datetime.now()

    db_session = sessionmaker(bind=engine)
    db = db_session()

    job_num = int(job_id.replace("JV-", ""))
    job = db.query(Job).filter(Job.id == job_num).first()

    if not job:
        console.print(f"[bold red]Error: Job with ID {job_id} not found.[/bold red]")
        db.close()
        raise typer.Exit(code=1)

    contact = Contact(
        job_id=job.id,
        date=contact_date.date(),
        type=type,
        person=person,
        notes=notes,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    db.close()

    console.print(f"[bold green]Added contact for Job ID {job_id} with {person}.[/bold green]")


result_app = typer.Typer()
app.add_typer(result_app, name="result", help="Manage job results/outcomes.")

@result_app.command("add")
def add_result(
    job_id: str = typer.Argument(..., help="Job ID (e.g., JV-0001)"),
    status: str = typer.Option(..., "--status", "-s", help="Status update (e.g., interview, offer, rejected)"),
    result_date: datetime = typer.Option(None, "--date", "-d", help="Date of result (YYYY-MM-DD)"),
    notes: str = typer.Option(None, "--notes", "-n", help="Notes about the result"),
):
    """
    Records a new result/outcome for a job application and updates job status.
    """
    if result_date is None:
        result_date = datetime.now()

    db_session = sessionmaker(bind=engine)
    db = db_session()

    job_num = int(job_id.replace("JV-", ""))
    job = db.query(Job).filter(Job.id == job_num).first()

    if not job:
        console.print(f"[bold red]Error: Job with ID {job_id} not found.[/bold red]")
        db.close()
        raise typer.Exit(code=1)

    result = Result(
        job_id=job.id,
        date=result_date.date(),
        status=status,
        notes=notes,
    )
    db.add(result)
    
    # Update job status
    job.status = status
    db.add(job) # Add the job object to the session to mark it for update
    
    db.commit()
    db.refresh(result)
    db.refresh(job) # Refresh job to get updated status
    db.close()

    console.print(f"[bold green]Recorded result for Job ID {job_id}. Status updated to {status}.[/bold green]")


@app.command()
def show_job(
    job_id: str = typer.Argument(..., help="Job ID (e.g., JV-0001)"),
):
    """
    Shows details for a specific job application, including contacts and results.
    """
    db_session = sessionmaker(bind=engine)
    db = db_session()

    job_num = int(job_id.replace("JV-", ""))
    job = db.query(Job).filter(Job.id == job_num).first()

    if not job:
        console.print(f"[bold red]Error: Job with ID {job_id} not found.[/bold red]")
        db.close()
        raise typer.Exit(code=1)

    console.print(f"\n[bold blue]Job Details for {job.title} at {job.company} (ID: JV-{job.id:04})[/bold blue]")
    console.print(f"  [bold]Applied Date:[/bold] {job.applied_date}")
    console.print(f"  [bold]Status:[/bold] {job.status}")
    console.print(f"  [bold]Source:[/bold] {job.source}")

    if job.contacts:
        console.print("\n[bold yellow]Contacts:[/bold yellow]")
        contact_table = Table("Date", "Type", "Person/Org", "Notes")
        for contact in job.contacts:
            contact_table.add_row(
                str(contact.date),
                contact.type,
                contact.person,
                contact.notes or "[N/A]",
            )
        console.print(contact_table)
    else:
        console.print("\n[italic red]No contacts recorded for this job.[/italic red]")

    if job.results:
        console.print("\n[bold magenta]Results:[/bold magenta]")
        result_table = Table("Date", "Status", "Notes")
        for result in job.results:
            result_table.add_row(
                str(result.date),
                result.status,
                result.notes or "[N/A]",
            )
        console.print(result_table)
    else:
        console.print("\n[italic red]No results recorded for this job.[/italic red]")
    
    db.close()

if __name__ == "__main__":
    app()
