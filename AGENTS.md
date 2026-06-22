# Repository Guidelines

## Project Structure & Module Organization

This repository is a GitHub Pages site. Keep public-facing pages and entry files at the repository root unless a framework-specific structure is introduced. Place reusable source code in `src/`, static assets in `assets/` or `public/`, and tests in `tests/` or next to the code they cover using a clear suffix such as `.test.js`.

Example layout:

```text
/
  index.html
  assets/
  src/
  tests/
```

## Build, Test, and Development Commands

This appears to be a plain static GitHub Pages site, so no build step is required unless tooling is added later. For local review, open `index.html` directly in a browser or serve the folder with a simple static server:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`. Use a local server when testing relative paths, fonts, images, or browser APIs that do not behave the same from `file://`.

## Coding Style & Naming Conventions

Use consistent, readable formatting with 2-space indentation for HTML, CSS, JavaScript, and JSON. Prefer lowercase, hyphenated filenames for pages and assets, such as `about.html` or `profile-card.css`. Keep CSS class names descriptive and scoped to the component or section they style.

Avoid unrelated formatting churn. If tooling such as Prettier, ESLint, or Stylelint is added later, document the command here and apply it consistently.

## Testing Guidelines

There is no formal test runner documented for this static site. For visual changes, verify pages manually in a browser at common desktop and mobile widths. Check navigation, images, external links, and console errors. If reusable JavaScript grows, add tests under `tests/` or with a `.test.js` suffix and document how to run them.

## Commit & Pull Request Guidelines

Use the cz commit style for commit messages. Prefer Conventional Commit-style scopes and types, for example:

```text
feat(site): add project gallery
fix(styles): correct mobile header spacing
docs(readme): update local setup notes
```

Pull requests should include a short description, linked issue if applicable, testing notes, and screenshots for UI changes. Keep each PR focused on one logical change.

## Agent-Specific Instructions

Before editing, inspect existing files and preserve local conventions. Do not revert unrelated user changes. Keep generated changes small, verify when possible, and update this guide when repository commands or structure change.
