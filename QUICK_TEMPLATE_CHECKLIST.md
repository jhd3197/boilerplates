# Quick Template Creation Checklist

Use this checklist when adding ANY new template.

## ✅ Pre-Creation

- [ ] Decide on category: `python`, `react`, `fullstack`, `node`, `vue`, etc.
- [ ] Decide on template name (lowercase with underscores)
- [ ] Know what files your template will include

## ✅ Create Directory

```bash
mkdir -p boilerplates/templates/<category>/<template_name>
cd boilerplates/templates/<category>/<template_name>
```

## ✅ Add Files with Placeholders

### For ALL templates, replace:

| Original | Placeholder | Used For |
|----------|-------------|----------|
| `myproject` | Keep as is (CLI replaces) | Code, imports, package names |
| `MyProject` | Keep as is (CLI replaces) | Comments, docstrings, titles |
| Author name | `AUTHOR_NAME_PLACEHOLDER` | metadata.py, headers |
| Author email | `AUTHOR_EMAIL_PLACEHOLDER` | metadata.py, headers |
| Description | `PROJECT_DESCRIPTION_PLACEHOLDER` | metadata.py, docs |
| Project name | `PROJECT_NAME_PLACEHOLDER` | Markdown titles |
| Package name | `PACKAGE_NAME_PLACEHOLDER` | Markdown code blocks |

### File-Specific Placeholders

**Python files (metadata.py):**
```python
NAME = "myproject"  # Package name (slug format)
DISPLAY_NAME = "PROJECT_DISPLAY_NAME_PLACEHOLDER"  # Original project name
VERSION = "1.0.0"
DESCRIPTION = "PROJECT_DESCRIPTION_PLACEHOLDER"
AUTHOR = "AUTHOR_NAME_PLACEHOLDER"
AUTHOR_EMAIL = "AUTHOR_EMAIL_PLACEHOLDER"
```

**Markdown files:**
```markdown
# PROJECT_NAME_PLACEHOLDER

This is PACKAGE_NAME_PLACEHOLDER...
```

**Docker files:**
```yaml
services:
  api:
    container_name: myproject_api
```

## ✅ Create template.json

**Minimum required:**

```json
{
  "id": "template_name",
  "name": "Human Readable Name",
  "description": "What this template provides",
  "prompts": {
    "project_name": {
      "label": "Project name",
      "default": "My Project",
      "format": "text"
    },
    "package_name": {
      "label": "Package name",
      "default": "myproject",
      "format": "snake_case"
    }
  },
  "rename": {
    "myproject": "{{package_name}}"
  },
  "replace": []
}
```

## ✅ Add Replace Patterns

**For Python templates:**

```json
"replace": [
  {
    "glob": "**/*.py",
    "values": {
      "myproject": "{{package_name}}",
      "MyProject": "{{project_name}}",
      "AUTHOR_NAME_PLACEHOLDER": "{{author_name}}",
      "AUTHOR_EMAIL_PLACEHOLDER": "{{author_email}}",
      "PROJECT_DESCRIPTION_PLACEHOLDER": "{{project_description}}",
      "PROJECT_DISPLAY_NAME_PLACEHOLDER": "{{project_name}}"
    }
  },
  { "glob": "*.py", "values": { /* same as above */ } },
  { "glob": "**/*.md", "values": { /* MyProject + PROJECT_NAME_PLACEHOLDER */ } },
  { "glob": "*.md", "values": { /* same as above */ } },
  { "glob": "**/*.yml", "values": { "myproject": "{{package_name}}" } },
  { "glob": "*.yml", "values": { "myproject": "{{package_name}}" } },
  { "glob": ".env*", "values": { "MyProject": "{{project_name}}" } }
]
```

**For React templates:**

```json
"replace": [
  {
    "glob": "**/*.{js,jsx,json,html}",
    "values": {
      "React App Name": "{{project_name}}"
    }
  },
  { "glob": "*.{js,json,html}", "values": { /* same */ } },
  { "glob": "**/*.md", "values": { /* documentation */ } },
  { "glob": "*.md", "values": { /* same */ } }
]
```

**For Fullstack templates:**

```json
"replace": [
  { "glob": "backend/**/*.py", "values": { /* Python replacements */ } },
  { "glob": "backend/*.py", "values": { /* Python replacements */ } },
  { "glob": "frontend/**/*.{js,jsx,json}", "values": { /* React replacements */ } },
  { "glob": "frontend/*.{js,json}", "values": { /* React replacements */ } },
  { "glob": "**/*.md", "values": { /* both */ } },
  { "glob": "*.md", "values": { /* both */ } },
  { "glob": "docker-compose.yml", "values": { "myproject": "{{package_name}}" } }
]
```

## ✅ Test Template

```bash
# List to verify it appears
boilerplates list

# Create test project
boilerplates create <category> <template_name> "Test Project"

# Navigate to output
cd output/test_project

# Check for unreplaced placeholders
grep -r "myproject" . --exclude-dir=node_modules --exclude-dir=venv
grep -r "MyProject" . --exclude-dir=node_modules --exclude-dir=venv
grep -r "PLACEHOLDER" . --exclude-dir=node_modules --exclude-dir=venv

# Should return NOTHING if all replaced correctly!
```

## ✅ Verify Files

- [ ] All `myproject` → replaced with slug
- [ ] All `MyProject` → replaced with original name
- [ ] All `*_PLACEHOLDER` → replaced with actual values
- [ ] Directory renamed if specified in `rename`
- [ ] Root-level files updated (*.py, *.md, *.yml in root)
- [ ] Nested files updated (**/*.py, **/*.md, etc.)
- [ ] Config files updated (.env, docker-compose.yml)

## ✅ Common File Types to Include

### Python Templates
- [ ] `requirements.txt`
- [ ] `setup.py`
- [ ] `.env.example`
- [ ] `app.py` or `main.py`
- [ ] `README.md`
- [ ] `how_it_works.md`
- [ ] `docker-compose.yml`
- [ ] `Dockerfile`
- [ ] Package directory with `__init__.py`, `metadata.py`

### React Templates
- [ ] `package.json`
- [ ] `vite.config.js` or `webpack.config.js`
- [ ] `index.html`
- [ ] `.env.example`
- [ ] `README.md`
- [ ] `Dockerfile`
- [ ] `src/` directory with components

### Fullstack Templates
- [ ] All Python files in `backend/`
- [ ] All React files in `frontend/`
- [ ] Root `docker-compose.yml`
- [ ] Root `README.md`
- [ ] Root `.gitignore`

## ✅ Final Checks

```bash
# Count files updated (should match your expectations)
boilerplates create <category> <template> "Test" 2>&1 | grep "Updated"

# Example: "Updated 18 files."

# Test the actual template works
cd output/test_project

# For Python:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# For React:
npm install
npm run dev

# For Fullstack:
docker-compose up --build
```

## 📊 Template Patterns Summary

| File Location | Pattern | Priority |
|---------------|---------|----------|
| Nested Python | `**/*.py` | High |
| Root Python | `*.py` | High |
| Nested Markdown | `**/*.md` | Medium |
| Root Markdown | `*.md` | High |
| All YAML | `**/*.yml`, `*.yml` | Medium |
| Env files | `.env*` | Low |
| Docker | `**/Dockerfile` | Low |

## 🚀 Quick Commands

```bash
# Create category
mkdir -p boilerplates/templates/<category>

# Create template
mkdir boilerplates/templates/<category>/<template_name>

# Test
boilerplates create <category> <template_name> "Test"

# Verify
cd output/test && grep -r "PLACEHOLDER\|myproject\|MyProject" .
```

---

**Remember:** Always test with `boilerplates list` and `boilerplates create` before committing!
