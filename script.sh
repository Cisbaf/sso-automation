#!/bin/bash

# Nome do projeto Celery
PROJECT_NAME="celery_app"

# Iniciar o worker
echo "Iniciando o Celery worker..."
celery -A $PROJECT_NAME worker --loglevel=info &

# Iniciar o Celery beat (scheduler)
echo "Iniciando o Celery beat..."
celery -A $PROJECT_NAME beat --loglevel=info &

# Iniciar o Flower
echo "Iniciando o Flower..."
celery -A $PROJECT_NAME flower --port=5555 &

# Informar que todos os serviços foram iniciados
echo "Todos os serviços foram iniciados."
