dev docker:
	docker compose -f docker-compose.dev.yml up --build

init migrations:
	docker exec -ti admin_panel_async_api python manage.py migrate

superuser in admin:
	docker exec -ti admin_panel_async_api python manage.py createsuperuser

staticfiles:
	docker exec -ti admin_panel_async_api python manage.py collectstatic

reload nginx:
	docker exec -ti nginx_async_api nginx -s reload