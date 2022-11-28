dev docker:
	docker compose -f docker-compose.dev.yml up --build

init migrations:
	docker exec -ti admin_panel_async_api python manage.py migrate