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
	@rm -f back/srcs/media/*
	@mv back/srcs/default.png back/srcs/media/
	@[ -e back/database.db ] && rm -f back/database.db || echo "database.db does not exist";
	@[ -e back/secret.key ] && rm -f back/secret.key || echo "secret.key does not exist";

re: clean all

insert:
	@$(MAKE) _insert COUNT=$(filter-out $@,$(MAKECMDGOALS))

_insert:
	@docker exec -it back python /app/srcs/insert_users.py $(COUNT)

.PHONY: all down clean re insert _insert