all:
	@docker-compose up -d --build
down:
	@docker compose down
clean:
	@rm back/database.db
	@docker stop $$(docker ps -qa);
	@docker rm $$(docker ps -qa);
	@docker rmi -f $$(docker images -qa);
	@docker volume rm $$(docker volume ls -q);
	@docker system prune -af;
	@mv back/srcs/media/jareste-.png back/srcs/
	@rm back/srcs/media/*
	@mv back/srcs/jareste-.png back/srcs/media/

migrations:
	@docker exec -it back python /app/crazy_pong/manage.py makemigrations
	@docker exec -it back python /app/crazy_pong/manage.py migrate