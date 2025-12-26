# Boilerplates

A collection of boilerplates for my projects.

## Project Structure

- `python/`: Python based templates.
  - `python_client_flask/`: A Flask application structure.
- `react/`: React based templates.
  - `react_spa/`: Client-only app (Vite, Router).
  - `react_dashboard/`: Auth, tables, charts, admin UI.
  - `react_marketing/`: Landing pages, SEO focused.
  - `react_embedded/`: Widgets embedded into other apps.

## Quick Start

To create a new project from a template, run the initialization script:

```bash
python init_project.py
```

Follow the interactive prompts to:
1. Select a template.
2. Name your new project directory.
3. Customize the internal package name (automatically cleans up `myproject` references).

## Template Configuration

Future templates will be defined using a JSON structure similar to this:

```json
{
  "id": "python_client_api",
  "name": "Python Client + API",
  "description": "Client-centric Python project with an integrated API server.",

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
      "glob": "**/*.{py,md}",
      "values": {
        "{{PROJECT_NAME}}": "{{project_name}}",
        "{{PACKAGE_NAME}}": "{{package_name}}"
      }
    }
  ]
}
```