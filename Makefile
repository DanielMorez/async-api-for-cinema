dev docker:
	docker-compose -f docker-compose.dev.yml up --build

prod docker:
	docker-compose -f docker-compose.prod.yml up --build

init migrations:
	docker exec -ti admin_panel_async_api python manage.py migrate
	docker exec -ti billing python manage.py migrate
	docker exec -ti auth flask db upgrade

superuser in admin:
	docker exec -ti admin_panel_async_api python manage.py createsuperuser

staticfiles:
	docker exec -ti admin_panel_async_api python manage.py collectstatic
	docker exec -ti notification-admin python manage.py collectstatic
	docker exec -ti billing python manage.py collectstatic

reload nginx:
	docker exec -ti nginx_async_api nginx -s reload

test:
	docker-compose -f async-api/tests/functional/docker-compose.yml up --build

auth:
	docker-compose -f docker-compose.dev.yml up -d --no-deps --build auth

nginx:
	docker-compose -f docker-compose.prod.yml up -d --no-deps --build nginx

ugc depends on:
	docker-compose -f docker-compose.dev.yml up -d postgres redis auth zookeeper broker broker-ui clickhouse

notification:
	docker-compose -f docker-compose.dev.yml up --build -d postgres redis auth notification-admin \
	notification-scheduler notification-api notification-worker
