FROM python:3.10.6

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

WORKDIR /app

ADD topicaxisapi /app/topicaxisapi
COPY pyproject.toml /app
COPY poetry.lock /app
ADD alembic /app/alembic
COPY alembic.ini.tmpl /app

RUN pip install poetry==1.4.2
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

ENV TOPICAXIS_API_CONFIG_FILE=/app/.env
EXPOSE 8000

COPY ./docker-entrypoint.sh /app
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["run"]
