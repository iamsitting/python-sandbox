---
name: django-add-app-basic
description: "Add a new feature app to an existing django-starter-project scaffold. Makes all structural assumptions automatically — no planning prompts. Use when adding CRUD features, list/detail views, or new sections to a Django project bootstrapped with the django-starter-project skill."
argument-hint: "What feature should the new app implement? (e.g. blog, tasks, products)"
---

# Django Add App (Basic)

Add a self-contained feature app to an existing Django project that was created with the `django-starter-project` skill. All structural, naming, and wiring decisions are made automatically based on the feature name provided.

Starter baseline this skill assumes:
- Stable Django release
- Bootstrap 5 via `django-bootstrap5`

## When to Use
- Extending a `django-starter-project` scaffold with a new feature
- Adding a CRUD section (list, detail, create, edit, delete) for any model
- Quickly scaffolding a new app without making architectural decisions

## Assumptions (No User Confirmation Needed)
This skill makes the following choices automatically:
- App lives at `apps/<feature>/` following the existing `apps/` convention
- Primary model is named after the feature in singular form (e.g. feature `blog` → model `Post`)
- Views use Django's class-based generic views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`)
- Templates live at `templates/<feature>/` and extend the existing `base.html`
- URL namespace matches the app label (e.g. `app_name = "blog"`)
- URLs are mounted at `/<feature>/` in the root URL conf
- Admin registration uses standard Django `ModelAdmin` with sensible `list_display`
- No additional packages are installed unless strictly required for the feature
- Login is required for create, update, and delete views; list and detail are public unless the feature name implies otherwise (e.g. `dashboard`, `profile`, `admin`)

## Output
A new `apps/<feature>/` app containing:
- `models.py` with a primary model and sensible fields inferred from the feature name
- `views.py` with the five standard generic views
- `urls.py` with named routes and the app namespace
- `admin.py` registered with standard Django admin
- `templates/<feature>/` with `list.html`, `detail.html`, `form.html`, and `confirm_delete.html`
- All templates extending `base.html` and using Bootstrap 5 components
- App wired into `INSTALLED_APPS` and the root URL conf

## Procedure
1. Derive the app label and model name from the argument (lowercase singular label, TitleCase model name).
2. Run `python manage.py startapp <feature>` and move the result to `apps/<feature>/`.
3. Update `apps/<feature>/apps.py` so `name = "apps.<feature>"`.
4. Add `"apps.<feature>"` to `INSTALLED_APPS` in `settings.py`.
5. Write the primary model in `models.py` with fields inferred from the feature name; always include `created_at` and `updated_at` timestamp fields and a `__str__` method.
6. Create `views.py` with `ListView`, `DetailView`, `CreateView`, `UpdateView`, and `DeleteView`; apply `LoginRequiredMixin` to write views.
7. Create `urls.py` with `app_name` set and URL patterns for all five views.
8. Mount the app URLs in the root `config/urls.py` at `/<feature>/`.
9. Register the model in `admin.py` with a `ModelAdmin` class; set `list_display` to the most relevant fields.
10. Create `templates/<feature>/` with the four standard templates, each extending `base.html` and using Bootstrap 5 cards, tables, or forms as appropriate.
11. Run `python manage.py makemigrations <feature>` and `python manage.py migrate`.
12. Verify the app with `python manage.py check` and confirm all five routes load in the browser.

## Model Field Inference Rules
When deriving model fields from the feature name, apply these defaults:
- Any feature → `title` (CharField), `created_at` (auto_now_add), `updated_at` (auto_now)
- Content-like features (blog, news, article) → add `body` (TextField) and `published` (BooleanField, default False)
- Task/todo-like features → add `description` (TextField, blank), `due_date` (DateField, null/blank), `done` (BooleanField, default False)
- Product/item-like features → add `description` (TextField, blank), `price` (DecimalField), `stock` (PositiveIntegerField)
- Event-like features → add `description` (TextField, blank), `start_at` (DateTimeField), `location` (CharField, blank)
- When uncertain, default to `title` + `description` (TextField, blank) + timestamps

## Template Conventions
- `list.html` — Bootstrap table or card grid with links to detail and create
- `detail.html` — Bootstrap card with all fields; links to edit and delete
- `form.html` — Bootstrap form using `{% bootstrap_form form %}` from `django-bootstrap5`; used for both create and update
- `confirm_delete.html` — Simple confirmation page with a POST form and a cancel link back to the list

## Admin Conventions
- Register using `@admin.register(<Model>)`
- Set `list_display` to `title` (or the primary identifying field), `created_at`, and any boolean flags
- Set `search_fields` to `["title"]`
- Set `list_filter` to boolean or date fields if present

## Completion Checks
- `python manage.py check` passes with no errors
- Migrations for the new app apply cleanly
- All five URL routes resolve without 404 or 500 errors
- List view renders with Bootstrap layout
- Create and update forms submit successfully
- Delete confirmation works and redirects to the list
- Admin list page for the new model loads correctly
- No changes were made to `core`, `accounts`, or `base.html`
