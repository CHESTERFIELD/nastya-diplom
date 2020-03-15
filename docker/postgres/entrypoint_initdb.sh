#!/bin/bash
psql -U postgres -c "CREATE USER persik PASSWORD 'qwerty123'"
psql -U postgres -c "CREATE DATABASE face_recog_db OWNER persik"
