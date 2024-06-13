all:
	@docker-compose up -d --build
down:
	@docker compose down
clean:
	@docker stop $$(docker ps -qa);
	@docker rm $$(docker ps -qa);
	@docker rmi -f $$(docker images -qa);
	@docker volume rm $$(docker volume ls -q);
	@docker system prune -af;
	@cp back/srcs/media/default.png back/srcs/
	@rm back/srcs/media/*
	@mv back/srcs/default.png back/srcs/media/
	@rm back/database.db

migrations:
	@docker exec -it back python /app/crazy_pong/manage.py makemigrations
	@docker exec -it back python /app/crazy_pong/manage.py migrate
