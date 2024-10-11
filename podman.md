All images are present on my quay.io account. https://quay.io/user/aleksander124/

```shell
podman pull quay.io/aleksander124/todo-application-front:latest
podman pull quay.io/aleksander124/todo-application-api:latest

podman network create backend
podman network create frontend

podman run -d --name database-prod --network=backend -e POSTGRES_DB=todo-app -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p 5432:5432 postgres
podman run -d --name api --network=backend -p 8000:8000 -e DB_USER=admin -e DB_PASSWORD=admin -e DB_NAME=todo-app -e DB_HOST=database-prod -e DB_PORT=5432 -e SECRET_KEY=secret-key quay.io/aleksander124/todo-application-api:latest
podman run -d --name frontend --network=frontend -p 3000:3000 -e API_URL=http://localhost:8000 quay.io/aleksander124/todo-application-front:latest
```