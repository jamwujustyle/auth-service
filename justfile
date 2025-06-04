# justfile

start:
    ./scripts/start-dev.sh

migrate:
    docker exec -it auth-service sh -c "aerich migrate"

upgrade:
    docker exec -it auth-service sh -c "aerich upgrade"

cli name:
    fastapi generate route {{name}}


seqres:
    docker exec -it auth-db psql -U dev -d auth-db -c "select setval('user_id_seq', 1, false);"

resdb:
    docker exec -it auth-db psql -U dev -d auth-db -c "delete from \"user\";"


stop:
    docker stop auth-service auth-db