# Boilerplate Manager Web App Plan

## Overview
A static web app hosted on GitHub Pages that lets users browse, customize, and download boilerplate templates directly in the browser.

## Why This Approach?

| Option | Pros | Cons |
|--------|------|------|
| **Flask/Python** | Familiar | Can't run on GitHub Pages (needs server) |
| **Go CLI** | Fast, single binary | Users must install, no web demo |
| **Static Web App** | Free hosting, instant demo, no install | All logic in browser |

**Winner: Static Web App** - Zero infrastructure, works on GitHub Pages, instant gratification for users.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Pages                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Static Web App                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │   │
│  │  │ Template │  │ Variable │  │   Download   │  │   │
│  │  │ Selector │→ │  Form    │→ │  Generator   │  │   │
│  │  └──────────┘  └──────────┘  └──────────────┘  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                 GitHub Raw Content                       │
│  • templates-registry.json                              │
│  • Template files (fetched on demand)                   │
└─────────────────────────────────────────────────────────┘
```

## Core Features

### Phase 1: MVP (Static Site)
- [ ] Browse templates by category (React, Python, PHP)
- [ ] View template details (description, tags, preview)
- [ ] Fill in variables (project name, author, etc.)
- [ ] Generate & download ZIP with replaced variables
- [ ] Mobile-responsive design

### Phase 2: Enhancements
- [ ] Template preview (file tree)
- [ ] Dark/light mode
- [ ] Search & filter templates
- [ ] Remember recent projects (localStorage)
- [ ] Share template links with pre-filled values

### Phase 3: Advanced
- [ ] GitHub OAuth - create repo directly
- [ ] Custom template import (paste GitHub URL)
- [ ] Template favorites

---

## Tech Stack Options

### Option A: Vanilla JS (Simplest)
```
webapp/
├── index.html
├── styles.css
├── app.js
└── jszip.min.js    # For creating ZIP files
```
**Pros:** No build step, tiny, fast
**Cons:** More manual DOM manipulation

### Option B: React + Vite (Modern)
```
webapp/
├── src/
│   ├── App.jsx
│   ├── components/
│   └── utils/
├── index.html
└── vite.config.js
```
**Pros:** Component-based, familiar if you know React
**Cons:** Build step required

### Option C: Astro (Best of Both)
```
webapp/
├── src/
│   ├── pages/index.astro
│   └── components/
└── astro.config.mjs
```
**Pros:** Static output, islands architecture, fast
**Cons:** Another framework to learn

**Recommendation:** Option A (Vanilla JS) for MVP, can migrate to React later if needed.

---

## How It Works

### 1. Fetch Registry
```javascript
const registry = await fetch('https://raw.githubusercontent.com/jhd3197/boilerplates/main/templates-registry.json')
```

### 2. User Selects Template
Shows cards with template info from registry

### 3. Fetch Template Files
```javascript
// Use GitHub API to get file tree
const tree = await fetch(`https://api.github.com/repos/jhd3197/boilerplates/git/trees/main?recursive=1`)

// Fetch each file in template path
const files = tree.filter(f => f.path.startsWith(templatePath))
```

### 4. Replace Variables
```javascript
// Read template.json for variable definitions
// Show form to user
// Replace {{variable}} patterns in file contents
```

### 5. Generate ZIP
```javascript
import JSZip from 'jszip';

const zip = new JSZip();
files.forEach(f => {
  const content = replaceVariables(f.content, userValues);
  zip.file(f.name, content);
});

const blob = await zip.generateAsync({type: 'blob'});
saveAs(blob, `${projectName}.zip`);
```

---

## File Structure (Final)

```
boilerplates/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml     # Deploy webapp to GitHub Pages
├── webapp/                       # New web app
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── app.js
│   │   ├── templates.js
│   │   └── zip-generator.js
│   └── assets/
│       └── logo.svg
├── templates/                    # Move here (root level)
│   ├── python/
│   ├── react/
│   └── php/
├── templates-registry.json
└── go-boilerplate-manager/       # Keep or remove (optional CLI)
```

---

## GitHub Pages Deployment

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: webapp

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

---

## Roadmap

### Week 1: Foundation
- [ ] Create webapp folder structure
- [ ] Basic HTML/CSS layout
- [ ] Fetch and display templates from registry
- [ ] Template selection UI

### Week 2: Core Functionality
- [ ] Dynamic form generation from template.json prompts
- [ ] Variable replacement logic
- [ ] ZIP generation with JSZip
- [ ] Download functionality

### Week 3: Polish
- [ ] Responsive design
- [ ] Loading states
- [ ] Error handling
- [ ] Deploy to GitHub Pages

### Week 4: Enhancements
- [ ] File tree preview
- [ ] Search/filter
- [ ] Dark mode
- [ ] Share links

---

## What to Do with Go CLI?

| Option | Recommendation |
|--------|----------------|
| **Keep both** | Web for demo/quick use, CLI for power users |
| **Archive Go** | Focus on web, CLI is bonus |
| **Remove Go** | Simplify repo, web-only |

**Recommendation:** Keep Go CLI in repo but don't actively develop it. Web app becomes the primary interface.

---

## Final Decisions

| Question | Decision |
|----------|----------|
| **Framework** | React + Vite |
| **Styling** | Tailwind CSS |
| **Domain** | `jhd3197.github.io/boilerplates` |
| **Go CLI** | Keep but archive (no active development) |

---

## Next Steps

1. ~~Answer the questions above~~ Done
2. Create React + Vite + Tailwind webapp
3. Build MVP (template list + download)
4. Deploy to GitHub Pages
5. Iterate based on feedback
