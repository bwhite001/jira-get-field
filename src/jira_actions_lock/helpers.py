import os
import re
import sys

import click
from git import InvalidGitRepositoryError, Repo


def get_jira_fields(client, project, ticket, field_name):
    client.set_ticket_and_project(project=project, ticket_no=ticket)
    request = client.get_issue_fields(fields=None)
    names_str = ", ".join(request['names'].values())
    assert field_name in request['names'].values(), f"Field with the name '{field_name}' was not found in the issue {project}-{ticket} \n found: {names_str}"
    (field_id,field_name) = next((item for item in request['names'].items() if item[1] == field_name), None)
    assert field_id in request['fields'], f"Unable to find value for '{field_name}' with the name '{field_id}'"
    return request['fields'][field_id]

def get_branch_name():
    """Git Branchname."""
    branch_name = git_branch_name()
    if branch_name is not None:
        return branch_name
    return None


def git_branch_name():
    """Interact with Repo."""
    try:
        repo = Repo(os.getcwd())
        branch = repo.active_branch
        return f"{branch}"
    except ImportError:
        click.secho("Invalid Working Directory", fg="red")
        sys.exit(0)
    except InvalidGitRepositoryError:
        click.secho("Invalid Working Directory", fg="red")
        sys.exit(0)


def match_ticket(project, branch):
    """Match digits after projectid and -."""
    match = project + r"-(\d+)"
    ticket_nums = re.findall(match, branch)
    if len(ticket_nums) == 1 and ticket_nums[0] != "":
        return ticket_nums[0]
    return None


def get_ticket_from_branchname(project) -> str:
    """Get Ticket From Branchname."""
    # get_branch_name()
    branch = get_branch_name()
    if project not in branch:
        return ""
    for project_id in [project.lower(), project.upper(), project]:
        match = match_ticket(project_id, branch)
        if match is not None:
            return match
    return ""
