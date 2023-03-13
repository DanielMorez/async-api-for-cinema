dev docker:
	docker-compose -f docker-compose.dev.yml up --build

prod docker:
	docker-compose -f docker-compose.prod.yml up --build

init migrations:
	docker exec -ti admin_panel_async_api python manage.py migrate
	docker exec -ti auth flask db upgrade

superuser in admin:
	docker exec -ti admin_panel_async_api python manage.py createsuperuser

staticfiles:
	docker exec -ti admin_panel_async_api python manage.py collectstatic
	docker exec -ti notification-admin python manage.py collectstatic

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

notification co-services:
	docker-compose -f docker-compose.dev.yml up --build -d postgres redis auth rabbitmq

notification for admin panel:
	docker-compose -f docker-compose.dev.yml up --build -d postgres redis auth rabbitmq notification-api \
	notification-scheduler notification-worker

notification for api:
	docker-compose -f docker-compose.dev.yml up --build -d postgres redis rabbitmq auth notification-admin-panel \
	notification-scheduler notification-worker

notification for scheduler:
	docker-compose -f docker-compose.dev.yml up --build -d postgres redis auth notification-admin-panel \
	notification-api notification-worker

notification for worker:
	docker-compose -f docker-compose.dev.yml up --build -d postgres redis auth notification-admin-panel \
	notification-scheduler notification-api
