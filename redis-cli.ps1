#per windows che non supporta redis, script per connettersi a redis-cli sfruttando il redis-cli del container
docker exec -it redis redis-cli -h localhost -p 6380 -a redis