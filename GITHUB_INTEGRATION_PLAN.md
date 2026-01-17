
# GitHub Integration Plan for Boilerplate Manager

## 1. Overview

This document outlines a plan to integrate the Boilerplate Manager with GitHub, allowing users to consume boilerplates from both public and private repositories. This will significantly enhance the tool's flexibility and power, enabling a decentralized and expandable boilerplate ecosystem.

The core idea is to extend the existing `boilerplates` command-line tool to:
-   Fetch a curated list of public boilerplates from a central JSON file.
-   Allow users to register and use their own private boilerplates from GitHub.
-   Use GitHub Personal Access Tokens (PATs) for authentication with private repositories.
-   Cache remote boilerplates locally to improve performance and support offline use.
-   Maintain the existing powerful template expansion and replacement logic.

## 2. Configuration and Data Storage

To manage public and private repositories, we will introduce a configuration file and a local cache.

### 2.1. Configuration File (`~/.boilerplates/config.json`)

A new configuration file will be created in the user's home directory to store settings and registered repositories.

**Structure:**

```json
{
  "github_token": "YOUR_GITHUB_PAT",
  "private_repos": [
    {
      "alias": "my-private-template",
      "url": "https://github.com/user/private-repo.git"
    }
  ],
  "public_repo_url": "https://raw.githubusercontent.com/some-org/boilerplates-public/main/public-templates.json"
}
```

-   **`github_token`**: The user's GitHub PAT. This will be set via a new CLI command.
-   **`private_repos`**: A list of private repositories registered by the user.
-   **`public_repo_url`**: The URL to the curated list of public boilerplates. This allows the list to be updated without updating the tool itself.

### 2.2. Local Cache (`~/.boilerplates/cache/`)

Remote boilerplates will be cloned into a local cache directory.

**Structure:**

```
~/.boilerplates/
|-- cache/
|   |-- github.com/
|   |   |-- user/
|   |   |   |-- my-private-repo/
|   |   |   |-- another-public-repo/
|-- config.json
```

This structure mirrors the repository URL, preventing naming conflicts and making it easy to locate cached repositories.

## 3. Authentication

For accessing private repositories, users will need to provide a GitHub Personal Access Token (PAT) with the `repo` scope.

### New CLI command: `boilerplates config set-token`

This command will securely prompt the user for their token and save it to the `config.json` file.

```bash
$ boilerplates config set-token
Enter your GitHub Personal Access Token: ********************
Token saved successfully.
```

The application will use this token when cloning or fetching private repositories.

## 4. Repository Management

### 4.1. Public Repositories

A new JSON file, `public-templates.json`, will be hosted in a public GitHub repository. This file will contain a list of curated, high-quality boilerplates that follow the established `template.json` standard.

**`public-templates.json` Structure:**

```json
{
  "templates": [
    {
      "category": "python",
      "name": "fastapi-starter",
      "description": "A FastAPI starter with SQLAlchemy and Alembic.",
      "url": "https://github.com/some-org/fastapi-starter.git",
      "author": "Some Org"
    }
  ]
}
```

The `boilerplates` tool will fetch this file and display the templates to the user.

### 4.2. Private Repositories

Users can add and remove their own private repositories.

#### New CLI command: `boilerplates repo add`

This command registers a new private repository.

```bash
$ boilerplates repo add <repo_url> --alias <alias>
# Example
$ boilerplates repo add https://github.com/my-user/my-react-template.git --alias my-react
```

This will add an entry to the `private_repos` list in `config.json`. The `alias` is optional and will default to the repository name.

#### New CLI command: `boilerplates repo remove`

This command removes a registered private repository.

```bash
$ boilerplates repo remove my-react
```

## 5. Core Logic Modifications (`cli.py`)

The existing `cli.py` will be refactored to support the new functionality.

### 5.1. `list_templates()`

This function will be updated to:
1.  Read the local `boilerplates/templates` directory as it does now.
2.  Fetch and parse `public-templates.json` from the `public_repo_url`.
3.  Read the `private_repos` from `~/.boilerplates/config.json`.
4.  Merge all three sources into a single list of available templates, categorized appropriately.

### 5.2. `create_project()`

This function will be modified to handle remote repositories:
1.  When a user selects a remote template, the tool will check if it's already cached in `~/.boilerplates/cache/`.
2.  If not cached, it will be cloned from the `url` using the configured GitHub token for authentication. The `git` command will be used via `subprocess`.
3.  If it is cached, it will be updated by pulling the latest changes.
4.  Once the template is available locally in the cache, the rest of the `create_project` logic will proceed as before, using the cached directory as the `template_path`.

## 6. Boilerplate Structure (`template.json`)

The requirements for a repository to be a valid boilerplate remain unchanged. It **must** contain a `template.json` file at the root with the necessary `prompts`, `rename`, and `replace` rules. This ensures that any repository can be a boilerplate, regardless of its name or original purpose, as long as it's configured correctly.

## 7. User Workflow

1.  **First-time setup**: The user runs `boilerplates config set-token` to store their GitHub PAT.
2.  **Adding a private boilerplate**: The user runs `boilerplates repo add <url>` to register a private template.
3.  **Listing templates**: The user runs `boilerplates list` or `boilerplates init`. They will see a combined list of local, public, and their registered private boilerplates.
4.  **Creating a project**: The user selects a template.
    -   If it's a remote template, it's downloaded/updated to the local cache.
    -   The `template.json` from the boilerplate is used to prompt for variables.
    -   The boilerplate is copied to the `output` directory, and the replacement/rename logic is applied.

## 8. Implementation Plan (High-Level)

1.  **Create configuration management**:
    -   Implement `get_config_path()`, `load_config()`, and `save_config()` functions.
    -   Create the `~/.boilerplates` directory on first run.
2.  **Implement `config` commands**:
    -   Add `config` subparser to `argparse`.
    -   Implement `set-token` command.
3.  **Implement `repo` commands**:
    -   Add `repo` subparser to `argparse`.
    -   Implement `add` and `remove` commands.
4.  **Refactor `list_templates()`**:
    -   Add logic to fetch public and private repo lists.
    -   Use `requests` library to fetch the public JSON file.
5.  **Refactor `create_project()`**:
    -   Add logic to identify remote templates.
    -   Implement the cloning/pulling mechanism using `subprocess.run(['git', 'clone', ...])`.
    -   Ensure the GitHub token is used for authentication with private repos.
6.  **Update `main()`**:
    -   Wire up the new commands.
7.  **Add dependencies**:
    -   Add `requests` to `requirements.txt`.
8.  **Write documentation**:
    -   Update `README.md` to explain the new GitHub integration features.

## 9. Security Considerations

-   The GitHub PAT will be stored in plain text in the `config.json` file. The file should have restrictive permissions (e.g., `600`). The user will be warned about this.
-   Repository URLs will be validated to prevent command injection.
-   The tool will not execute any code from the downloaded boilerplates directly. It will only perform copy, rename, and replace operations.

This plan provides a comprehensive roadmap for a powerful new feature. By leveraging GitHub, the Boilerplate Manager can become a collaborative and highly personalized tool for developers.
