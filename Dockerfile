FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN useradd -ms /bin/bash docker-user

RUN apt-get -y update \
    && apt-get install -y gettext git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN curl -sSl https://install.python-poetry.org | POETRY_HOME=/opt/poetry POETRY_VERSION=1.2.2 python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install

COPY ./code .

RUN chown -R docker-user:docker-user /code
USER docker-user
