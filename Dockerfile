FROM python:3.12

WORKDIR /src

COPY poetry.lock pyproject.toml /src/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /src

ENTRYPOINT hypercorn --reload --bind 0.0.0.0:5050 --workers 1 app:app

EXPOSE 5050