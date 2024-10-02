#!/bin/bash

export NEO4J_PASS=databasenew

docker run -d -p 7474:7474 -p 7687:7687 --env NEO4J_AUTH="neo4j/${NEO4J_PASS}" neo4j
docker ps

echo "Ожидание запуска Neo4j..."

if [ ! -d "team00" ]; then
    sudo apt update
    sudo apt install -y python3.10-venv
    python3 -m venv team00
fi

source team00/bin/activate

pip install -r requirements.txt

python3 cache_wiki.py -p 'Erdős number' -d 3

# deactivate

echo "Скрипт завершен."
