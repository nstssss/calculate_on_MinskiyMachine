FROM python:3.10-slim
#установка рабочей директории внутри контейнера
WORKDIR /app
#установка записимостей
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# копирование исходного кода проекта в рабочую директроию контейнера
COPY . /app
# создание директории для хранения данных
RUN mkdir -p /data
# запуск контейнера
CMD ["/bin/sh", "-c", "\
    if [ ! -f /data/history.db ]; then \
        echo 'Копирую базу данных на хост...'; \
        cp /app/history.db /data/history.db; \
    fi; \
    python minsky_consoleAPP.py \
"]
