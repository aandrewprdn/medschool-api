FROM python:3.12-bullseye

RUN apt-get update

RUN apt-get -y install sudo unzip curl git snap

COPY ./README.md ./README.md
COPY ../pyproject.toml ./pyproject.toml
COPY ../poetry.lock ./poetry.lock

COPY ../src ./src
COPY ../web ./web

RUN pip install --no-cache-dir --upgrade poetry

RUN poetry install --no-cache --no-interaction --no-ansi

RUN echo "Checking for env" && poetry env list && poetry show

COPY --chmod=755 ./docker/ecs/run-web.sh /usr/src/app/run-web.sh

ENV PATH="/root/.local/bin:$PATH"

EXPOSE 3000

CMD ["/usr/src/app/run-web.sh"]