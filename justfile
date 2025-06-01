# justfile

run:
    uvicorn app.index:app --reload



migrate:
    docker exec -it auth-service sh -c "aerich migrate"

upgrade:
    docker exec -it auth-service sh -c "aerich upgrade"

cli name:
    faskapi generate route {{name}}