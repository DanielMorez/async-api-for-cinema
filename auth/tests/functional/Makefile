create-superuser:
	docker exec -it auth flask create-superuser pytest_superuser

tests:
	docker compose up --build -d
	docker exec -ti auth_test flask db upgrade
	docker restart tests
	docker-compose logs --tail=1 tests