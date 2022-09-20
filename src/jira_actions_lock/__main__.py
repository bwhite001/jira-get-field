#!/usr/bin/python
"""Process open MRs and notify the team."""
import click
import os
import sys

from jira_actions_lock import helpers
from jira_actions_lock import JiraClient

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL", "https://infoxchange.atlassian.net")
JIRA_USER_EMAIL = os.environ.get("JIRA_USER_EMAIL", "")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")
AUTH_HEADER = JIRA_USER_EMAIL + ":" + JIRA_API_TOKEN

assert (
    JIRA_USER_EMAIL != ""
), f"You must provide a JIRA_USER_EMAIL with access to {JIRA_BASE_URL}"
assert (
    JIRA_API_TOKEN != ""
), f"You must provide a JIRA_API_TOKEN with access to {JIRA_BASE_URL}"
assert AUTH_HEADER != ":", "You must provide a valid AUTH_HEADER"


@click.command()
@click.argument("project_id")
@click.argument("field_name")
@click.option("-r", "--required", is_flag=True, default=False)
@click.option("--ticket_override", default=None)
def main(project_id=None, field_name=None, required=False, ticket_override=None):
    """Fetch the ticket field from the Branchname."""
    jira_client = JiraClient(base_url=JIRA_BASE_URL, auth_header=AUTH_HEADER)
    assert project_id, "Project Id must be specified, eg SRS"
    assert field_name, "Field name must be specified, eg Release Notes"
    if project_id is not None:
        ticket = ticket_override
        if ticket_override is None:
            ticket = helpers.get_ticket_from_branchname(project_id)
        if ticket is None:
            click.echo("Could not find ticket")
            if required:
                sys.exit(1)
            else:
                sys.exit(0)
        else:
            field_value = helpers.get_jira_fields(
                jira_client, project_id, ticket, field_name
            )
            if field_value is None or field_value == "":
                click.echo("Could not find field value in ticket")
                if required:
                    sys.exit(1)
                else:
                    sys.exit(0)

            click.echo(f"{field_name}: {field_value} in {jira_client.browse_url}")
            sys.exit(0)


if __name__ == "__main__":
    main()
