# Product Catalog

Django application that models categories, tags and products, and has a single server-rendered page to search and filter products by description, category, and tags, with the ability to combine filters.

## Stack

- python 3.12, Django 6.0
- postgreSQL 16
- Gunicorn + WhiteNoise (for static files)
- Docker (compose)

## Features

- Three models with the following relationships: Product → Category (foreign key) and Product ↔ Tag (many to many).
- Search products by description (simple case-insensitive substring match).
- Filter by category (single select) and by tags (multi-select).
- Filters can be combined for narrow result pool and are sticky (selections persist after submitting).
- Something I did that was not required: result count and a clear filters button link.
- All models are registered and cofigured in Django admin panel (create, remove, edit entries, and perform search with filters).
- Seed management command to populate sample data.

## Setup & run

To run this project all you need is docker compose

# 1. Clone the repo
```
git clone https://github.com/useryt0/remarcableTest.git
cd remarcableTest
```
# 2. Create the environment file (replace with your own values)
```
cp .env.example .env
```
# 3. Build and start (Postgres + web containers). Django migrations run automatically.
```
docker compose up -d --build 
```
**note:** If you encounter port allocation problems, simply replace only the left port value in line 7 of docker-compose.yml with any valid port number

Then open http://localhost:8000/ (or your other port if you changed it)

## Data population
Sample data is loaded with the seed management command (catalog/management/commands/seed.py), which wipes and recreates 5 categories, 10 tags, and 20 products. You can also populate the database yourself using admin panel.
```
docker compose exec web python manage.py seed
```

### Admin

```bash
docker compose exec web python manage.py createsuperuser
```
Enter credentials for superuser
Then visit http://localhost:8000/admin/ to access the Django admin panel.

## Assumptions that were taken during development

Since some things were not exactly clarified in the assignment document, I made some assumptions:

- Search matches the product using description only, it is case-insensitive, partial match. Empty or only whitespace inputs results in no search filter being applied.
- Category filter is single-select, because a product can belong to only one category.
- Tag filter uses OR logic, which means that selecting multiple tags returns products matching any single one of them. Tags are supposed to help a user find an item, not narrow down their possible result pool. (AND would be a chained .filter(tags=[tag]) per tag.)
- Deleting a category sets affected products' category field to NULL (by setting on_delete=SET_NULL) rather than deleting the products. This is to prevent accidental deletion of related products.
- PostgreSQL is used rather than SQLite, to be more close to real production-grade stack. Assuming that DB is containerized.

## Design choices that were used

- Query logic is isolated in catalog/selectors.py, in order to keep the views thin. This allows the filtering logic to be reusable and testable in isolation, and easy to expose in the future via an API later without needing to rewrite or add extra logic .
- Query performance:  product queryset uses select_related('category') (FK → JOIN) and prefetch_related('tags') (M2M → separate query) to avoid N+1 problem when rendering the list. The tag filter uses .distinct() because filtering operation across a many-to-many relationship can return duplicate rows. The admin views apply the same idea via list_select_related and a prefetching get_queryset.
- Filters combine as AND (search AND category AND tags), each applied only if provided by the user.
- Static files are served by WhiteNoise so the app is runnable using Gunicorn.

## Project structure

```
catalog/
  models.py         #Category, Tag, Product models with relationships
  selectors.py      #separate read-only querying functions
  views.py          #thin view: it reads GET params, calls selectors, and renders the response
  urls.py           #path for the page
  admin.py          #admin registration + ability to edit records
  templates/catalog/product_list.html #templates
  management/commands/seed.py   #command for sample data creation
config/             #Default Django project and config
Dockerfile
docker-compose.yml
entrypoint.sh       # script that runs migrate command, runs collectstatic, then starts Gunicorn
```

## AI usage

As stated by the AI policy of this assignment, AI tools were occasionally used to assist me for some parts of this project, like HTML page scaffolding, startup troubleshooting (whitenoise wiring), seeding example data, and revising and styling this README file. All core logic and code including data models, query/selector logic, view, and the resulting template were composed by the me, and I confirm that I understand and take full responsibility for all code in this repository.
