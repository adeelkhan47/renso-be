FROM python:3.9

RUN mkdir /app/
WORKDIR /app/

COPY src /app/src/
COPY etc /app/etc/
COPY static /app/static
COPY poetry.toml poetry.lock pyproject.toml /app/

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

COPY docker-entrypoint.sh /usr/bin/

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]


