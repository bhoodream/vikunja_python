import click
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
import sys
import os
from dotenv import load_dotenv

load_dotenv()

console = Console()

class VikunjaClient:
    def __init__(self, url: str, token: str):
        self.url = url.rstrip('/')
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

    def _get(self, endpoint: str, exit_on_error: bool = True) -> dict:
        try:
            response = requests.get(f"{self.url}/api/v1/{endpoint}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if exit_on_error:
                console.print(f"[red]Error communicating with Vikunja API: {e}[/red]")
                sys.exit(1)
            raise

    def get_projects(self) -> list:
        return self._get("projects")

    def get_project_tasks(self, project_id: int) -> list:
        try:
            return self._get(f"projects/{project_id}/tasks", exit_on_error=False)
        except requests.exceptions.RequestException:
            return []

def format_date(date_str: str) -> str:
    if not date_str or date_str == "0001-01-01T00:00:00Z":
        return ""
    try:
        # Parse ISO format, handling Z timezone
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return date_str

def is_overdue(due_date_str: str) -> bool:
    if not due_date_str or due_date_str == "0001-01-01T00:00:00Z":
        return False
    try:
        dt = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        return dt < datetime.now(dt.tzinfo)
    except ValueError:
        return False

@click.command()
@click.option('--url', envvar='VIKUNJA_URL', required=True, help='URL of the Vikunja instance (e.g., https://vikunja.example.com)')
@click.option('--token', envvar='VIKUNJA_TOKEN', required=True, help='API Token for authentication')
def main(url: str, token: str):
    """Vikunja CLI Task Viewer"""
    client = VikunjaClient(url, token)
    
    with console.status("[bold green]Fetching data from Vikunja..."):
        projects = client.get_projects()

    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    # Map projects by ID
    project_map = {p['id']: p['title'] for p in projects}
    
    # Group tasks by project
    tasks_by_project = {}
    
    # Fetch tasks per project
    with console.status("[bold green]Fetching tasks per project..."):
        for project in projects:
            project_tasks = client.get_project_tasks(project['id'])
            if project_tasks:
                tasks_by_project[project['id']] = project_tasks

    # Display tasks
    for project_id, project_tasks in tasks_by_project.items():
        project_title = project_map.get(project_id, "Unknown Project")
        
        if not project_tasks:
            continue

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Title")
        table.add_column("Status", width=10)
        table.add_column("Due Date", justify="right")

        for task in project_tasks:
            task_id = str(task.get('id', ''))
            title = task.get('title', '')
            done = task.get('done', False)
            due_date = task.get('due_date', '')
            
            status = "[green]Done[/green]" if done else "[blue]Open[/blue]"
            
            due_date_formatted = format_date(due_date)
            
            if not done and is_overdue(due_date):
                due_date_formatted = f"[bold red]{due_date_formatted}[/bold red]"
                title = f"[bold red]{title}[/bold red]"
                status = "[bold red]Overdue[/bold red]"

            table.add_row(task_id, title, status, due_date_formatted)

        console.print(Panel(table, title=f"[bold cyan]{project_title}[/bold cyan]", expand=False))

if __name__ == '__main__':
    main()
