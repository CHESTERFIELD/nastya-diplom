#!/bin/bash
docker exec -it diplom_diplom-django-server_1 bash

# In new system user has to create new db in docker postgres container
# docker exec -it postgres-container createdb -U persik face_recog_db
# test