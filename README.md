# Jira Check Command
### example output:

```shell
$ 
Release Note: javascript package manager house keeping. in {Jira Url}
```

## Build Local

Requirments:
  - poetry
  - pip

Clone repo

```shell
  poetry build
  pip install dist/jira_actions_lock-{current_version}.whl

```
run using the command `jira_check`

```shell
jira_check $TICKET_NO $FIELDNAME
```

## Action Spec:

### Enviroment variables
- `JIRA_BASE_URL` - URL of Jira instance. Example: `https://jira.atlassian.net` (optional)
- `JIRA_API_TOKEN` - **Access Token** for Authorization. Example: `HXe8DGg1iJd2AopzyxkFB7F2` ([How To](https://confluence.atlassian.com/cloud/api-tokens-938839638.html))
- `JIRA_USER_EMAIL` - email of the user for which **Access Token** was created for . Example: `human@example.com`

### Arguments
- `projectId` - The project ID or Jira Prefix example `AMD`
- `fieldName` - The field name in the ticket. example `Release Note`
