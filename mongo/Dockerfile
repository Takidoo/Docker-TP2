FROM mongodb/mongodb-community-server:8.0-ubi8-slim

USER mongod

COPY ./mongo-init.js /docker-entrypoint-initdb.d/

EXPOSE 27017