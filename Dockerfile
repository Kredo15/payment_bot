FROM python:3.11-slim

ENV PYTHONPATH=/app

RUN apt-get update
# Удаляем кэшированные списки пакетов APT
RUN rm -rf /var/lib/apt/lists/*
# Создаём рабочую директорию
WORKDIR /app

# install poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy dependencies
COPY pyproject.toml poetry.lock ./

# install packages
RUN poetry install --no-interaction --no-root

# Копируем файлы проекта в контейнер
COPY . .

# Запускаем проект с использованием виртуального окружения
RUN chmod +x ./bin/entrypoint.sh

ENTRYPOINT ["./bin/entrypoint.sh"]