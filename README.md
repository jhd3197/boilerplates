# ⚡ Boilerplates CLI

> **Accelerate your development.** A powerful CLI for scaffolding production-ready projects in seconds.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

**Boilerplates** is a robust project generator designed to eliminate setup fatigue. Whether you are building a Flask API or a React Dashboard, get started with best-practice architectures instantly.

## Key Features

* **Interactive CLI:** Guided prompts make setup effortless.
* **Fuzzy Search:** Instantly find the template you need without memorizing names.
* **Smart Context:** Automatically handles slug conversion (e.g., "My App" → `my_app`).
* **Auto-Documentation:** Generates a custom `how_it_works.md` for every new project.
* **Highly Configurable:** Define custom prompts and file replacements via `template.json`.
* **Agents Ready:** Ready to be used with LLM Agents.  

---

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+**: Required to run the CLI.
*   **pip**: Python package installer.
*   *(Optional)* **Node.js & npm**: Required if you plan to use React templates.

---

## Installation

Clone the repository and install the CLI globally using pip. We recommend installing in editable mode so you can easily update templates.

### 1. Clone the repository
```bash
git clone https://github.com/jhd3197/boilerplates.git
cd boilerplates
```

### 2. Install the CLI
```bash
pip install -e .
```

> **Note:** If you get a "permission denied" error, try using `sudo` (Linux/Mac) or run your command prompt as Administrator (Windows).

### 3. Verify Installation
```bash
boilerplates --help
```

---

## Quick Start

### Interactive Mode (Recommended)

The easiest way to start a new project. The CLI will guide you through naming, metadata, and template selection.

```bash
boilerplates init
# or simply
boilerplates
```

**The Setup Wizard will collect:**

1.  **Project Name** (Auto-slugified for package names)
2.  **Author Metadata** (Name/Email)
3.  **Category** (Python, React, etc.)
4.  **Template Selection** (via Fuzzy Search)

### Non-Interactive Mode

Perfect for scripts or power users who know exactly what they want.

```bash
# Syntax: boilerplates create <category> <template_id> <project_name>

# Create a Python Flask project
boilerplates create python python_client_flask my-flask-app

# Create a React SPA
boilerplates create react react_spa my-react-app

# Custom flags
boilerplates create python python_client_flask my-app --package custom_pkg_name
boilerplates create react react_dashboard admin-panel --output ~/projects
```

To see a full list of commands:

```bash
boilerplates list
```

---
## GitHub Integration

Extend the power of the Boilerplate Manager by connecting it to GitHub. You can use a curated list of public boilerplates or add your own private repositories.

### 1. Configure Your GitHub Token

To use private repositories, you need to provide a GitHub Personal Access Token (PAT) with the `repo` scope.

```bash
boilerplates config set-token
```

The CLI will prompt you to enter your token, which will be stored securely in the tool's configuration.

### 2. Manage Repositories

#### Public Repositories
The tool comes pre-configured with a list of public boilerplates. This list is fetched from a central repository, so it can be updated without requiring a CLI update.

#### Private Repositories
You can add and remove your own private boilerplates.

**Add a repository:**
```bash
# Syntax: boilerplates repo add <repo_url> --alias <alias>
boilerplates repo add https://github.com/my-user/my-react-template.git --alias my-react
```
The `alias` is a short name you'll use to refer to the template. If you don't provide one, it will be inferred from the URL.

**Remove a repository:**
```bash
# Syntax: boilerplates repo remove <alias>
boilerplates repo remove my-react
```

Now, when you run `boilerplates list` or `boilerplates init`, you will see your private templates listed under the "private" category.

---

## Template Catalog

### Python

| Template ID | Description |
| --- | --- |
| `python_client_flask` | Modular Flask architecture with API structure. |
| `cache` | Standalone custom caching utilities. |
| `custom_cache` | Advanced caching implementation for high-performance needs. |
| `myproject` | Basic, unopinionated Python project structure. |

### React

| Template ID | Description |
| --- | --- |
| `react_spa` | Modern Single Page Application (Vite + React Router). |
| `react_dashboard` | Admin dashboard boilerplate with auth flows and charts. |
| `react_marketing` | High-performance landing page structure optimized for SEO. |
| `react_embedded` | Lightweight setup for embeddable widgets/scripts. |

---

## Template Configuration

Want to add your own templates? Each template acts as a blueprint. You can control how the CLI interacts with your template using a `template.json` file in the template's root.

### The `template.json` Schema

This file handles dynamic variable collection, file renaming, and string replacement.

```json
{
  "id": "python_client_flask",
  "name": "Python Client + Flask API",
  "description": "Client-centric Python project with an integrated Flask API server.",
  
  "prompts": {
    "project_name": {
      "label": "Project name",
      "default": "My Project",
      "format": "text"
    },
    "package_name": {
      "label": "Python package name",
      "default": "myproject",
      "format": "snake_case"
    }
  },
  
  "rename": {
    "myproject": "{{package_name}}"
  },
  
  "replace": [
    {
      "glob": "**/*.{py,md,txt}",
      "values": {
        "myproject": "{{package_name}}"
      }
    }
  ]
}
```

### Configuration Options

*   **Prompts:** Define input variables (`label`, `default`, `format`).
*   **Rename:** Map directory/file names to variables using `{{mustache}}` syntax.
*   **Replace:** Targeted string replacement within files using glob patterns.

> [!WARNING]
> **Legacy Mode:** If `template.json` is missing, the CLI defaults to "Legacy Mode." It will assume the project contains a folder named `myproject` and attempt to rename it and replace string instances with the new package name automatically. **This is deprecated.**

---

## Project Structure

```text
boilerplates/
├── boilerplates/           # Main Package Source
│   ├── __init__.py
│   ├── cli.py              # CLI Logic & Entry Point
│   └── templates/          # Template Repository
│       ├── python/
│       └── react/
├── setup.py                # Package Configuration
├── requirements.txt        # Dependencies
└── README.md
```

## Troubleshooting

**Command not found?**
Ensure your Python scripts directory is in your system's `PATH`.
*   **Windows**: Add `%APPDATA%\Python\Scripts` to PATH.
*   **Mac/Linux**: Add `~/.local/bin` to your PATH.

**Permission errors?**
Try running with `sudo` or check directory permissions.

---

## Documentation

Every project generated by **Boilerplates** comes with a specialized `how_it_works.md`. This auto-generated file provides immediate context for the specific template used, covering:

*   Project Structure breakdown
*   Dependency installation
*   Key features & technologies
*   Customization guides

---

Made with ❤️ by [Juan Denis](https://juandenis.com)
