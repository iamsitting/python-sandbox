---
name: django-starter-project
description: "Bootstrap a starter Django project with SQLite, built-in authentication, login/logout, a modern theme, and modular app structure. Use for new Django scaffolds, starter apps, and project setup workflows."
argument-hint: "What should the Django starter be called?"
---

# Django Starter Project

Create a clean, modular Django starter that is ready for future features.

## When to Use
- Starting a new Django project from scratch
- Setting up local development with SQLite
- Adding built-in authentication with login and logout
- Creating a modern-looking starter UI
- Preparing a codebase that future skills can extend with additional apps and features

## Output
A starter project that includes:
- A supported, stable Python and Django version
- Local SQLite database configuration
- Built-in auth with login and logout flows
- Django's built-in template engine with a shared `base.html`
- Bootstrap 5 (via `django-bootstrap5`) for layout and components
- A modern base theme and responsive templates
- A modular app layout with clear extension points

## Core Principles
- Prefer a current stable Django release, not prerelease or RC builds
- Use a supported Python version that matches the chosen Django release
- Keep the project deliberately small and easy to extend
- Put feature code in separate apps so later skills can add capabilities without rewriting the starter
- Keep settings, templates, static files, and URLs organized from the start

## Recommended Project Shape
- Project package: `config` or a similarly neutral root package
- Feature apps: `apps/core` and `apps/accounts` by default
- Shared templates: `templates/`
- Shared static assets: `static/`
- Local database: `db.sqlite3`

## Virtual Environment
- Create the virtual environment using `python -m venv .venv` inside the project root
- Name the directory `.venv` so it is consistently ignored by version control and VS Code picks it up automatically as the interpreter
- Activate with `source .venv/bin/activate` on macOS/Linux before running any project commands
- Add `.venv/` to `.gitignore` immediately
- Pin all direct dependencies in a `requirements.txt` at the project root using `pip freeze > requirements.txt` once the initial install is complete
- Never install project packages outside the virtual environment

## Procedure
1. Choose a short, neutral project name that reflects the starter purpose.
2. Create the virtual environment at `.venv`, activate it, and install a stable Django release, `django-bootstrap5`, and any only-when-needed starter dependencies. Pin them to `requirements.txt`.
3. Use Django's built-in admin with default styling unless a different admin theme is explicitly requested.
4. Start the project with a modular layout so apps live under a dedicated `apps/` package.
5. Create a `core` app for the landing page, health check, and general shell views.
6. Create an `accounts` app for authentication-related pages and URLs.
7. Configure `settings.py` for SQLite, templates, static files, login redirects, and installed apps.
8. Wire root URLs so the project exposes home, login, logout, and any starter pages cleanly.
9. Add a base template with a modern visual style and shared navigation.
10. Use built-in Django auth views for login and logout unless there is a clear reason to customize them.
11. Ensure templates exist for the auth flow and that logout returns to a sensible page.
12. Keep the starter theme self-contained and easy to restyle later.
13. Run migrations, verify the server starts, and confirm login/logout works end to end.

## Modularization Rules
- Keep each future feature in its own app unless it is obviously shared shell behavior
- Put reusable project-wide behavior in `core`
- Put authentication and profile behavior in `accounts`
- Add new apps by following the same `apps/<feature>` pattern
- Keep app URLs and templates local to each app when possible
- Avoid collapsing new feature work into the project package itself

## Templating
- Use Django's built-in template engine; no Jinja2 unless explicitly requested
- All templates live under the top-level `templates/` directory
- Use a single `base.html` with named blocks (`title`, `content`, `extra_css`, `extra_js`) so child templates can extend it cleanly
- Keep app-specific templates under `templates/<app_name>/` to avoid name collisions

## CSS Library
- Use Bootstrap 5 via the `django-bootstrap5` package for consistent, responsive layouts
- Load the Bootstrap CSS and JS through the `{% bootstrap_css %}` and `{% bootstrap_javascript %}` template tags provided by the package
- Avoid pinning to the absolute latest Bootstrap minor; use the version recommended by the current `django-bootstrap5` release
- Keep custom overrides in a project-level `static/css/custom.css` file that is loaded after Bootstrap so it is easy to restyle later

## Theme Guidance
- Use a modern, restrained aesthetic rather than a default Django look
- Rely on Bootstrap utility classes and components for spacing, typography, and navigation
- Keep the starter neutral enough that later skills can replace the palette or branding easily
- Build around reusable blocks in `base.html` so new pages can inherit the same shell

## Completion Checks
- `python manage.py check` passes
- Migrations apply cleanly against SQLite
- A browser can reach the landing page with Bootstrap styles applied
- Login and logout both work using the built-in auth flow
- Django admin renders correctly using the built-in admin app
- `base.html` blocks are in place and child templates extend correctly
- The app structure is still modular and ready for future skills to extend

## Handoff for Future Skills
When another skill needs to add features, it should:
- Reuse the existing `apps/` layout
- Add a new app instead of expanding the starter app indefinitely
- Preserve the login/logout and base template structure
- Extend the existing theme rather than replacing the scaffold

## Branding
- This starter is intended for an Information Systems Portal.
- Keep authentication and the `accounts` app in place as shared application context.
