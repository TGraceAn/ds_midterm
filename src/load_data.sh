redis-server --port 1111 &
cat redis.config | redis-server - --port 2222 &
cat redis.config | redis-server - --port 3333 &

redis-cli -p 1111 < actors.redis
