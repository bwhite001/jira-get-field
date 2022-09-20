import os
import base64
import requests
import click


class JiraClient:
    """Client to talk to jira_client."""
    base64_message = None
    def __init__(self,auth_header = "", base_url = "https://infoxchange.atlassian.net"):
        self.base_url = base_url
        if auth_header == "" or auth_header == ":":
            click.secho(
                "JIRA authentication header not found, set JIRA_AUTH_HEADER environment variable.",
                fg="red",
            )
            ctx = click.get_current_context()
            click.echo(ctx.get_help())
            ctx.exit()
        message_bytes = auth_header.encode("ascii")
        self.encode = base64.b64encode(message_bytes)
        base64_bytes = self.encode
        base64_message = base64_bytes.decode("ascii")
        self.headers = {"Authorization": "Basic " + base64_message}

    def _request(self, url):
        response = requests.get(url=url, headers=self.headers)
        res = response.json()
        if response.status_code != 200:
            click.secho(url, fg="blue")
            message = ""
            if "errorMessages" in res:
                message = "Response Error "
                message += str(response.status_code)
                message += ": "
                message += " ".join(res["errorMessages"])
            click.secho(message, fg="red")
            exit(1)
        return res

    def set_ticket_and_project(self, project, ticket_no):
        self.ticket_no = ticket_no.strip()
        self.project = project.strip()
        self.api_issue_url = f"{self.base_url}rest/api/2/issue/{project}-{ticket_no}"
        self.browse_url = f"{self.base_url}browse/{project}-{ticket_no}"
        self.formatter = None

    def get_issue_fields(self, fields="summary,description,issuetype"):
        """Request to JiraClient."""
        url = self.api_issue_url + "?expand=names,renderedFields"
        response = self._request(url)
        assert "names" in response, "Could not parse names in ticket response"
        assert "renderedFields" in response, "Could not parse renderedFields in ticket response"
        return {'fields':response['renderedFields'], 'names': response['names']}

    def get_response(self, path):
        """Request to JiraClient."""
        url = self.base_url + path
        return self._request(url)