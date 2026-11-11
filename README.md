# Custodian IAM

Identity access management web app built with Django and Pandas. It reads HR, role-based access control (RBAC) and daily activity spreadsheets and exposes dashboard views for user groups, application access and daily data.

## Structure
- `custodian/`: Django project settings and URLs
- `dashboard/`: app with the views (group handling, application lookup, RBAC applications, daily data) and templates
- `Resources/`: sample spreadsheets with dummy data (HR sheet, RBAC sample, paths, daily sheet)

## Run locally
```bash
pip install django pandas openpyxl
python manage.py migrate
python manage.py runserver
```

The spreadsheets in `Resources/` contain dummy data only.

## Stack
Python, Django, Pandas
