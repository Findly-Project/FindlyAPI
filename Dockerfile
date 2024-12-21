FROM python:3.12

WORKDIR /src

COPY poetry.lock pyproject.toml /src
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /src

EXPOSE 5000

CMD ["/bin/bash", "-c", "python app.py"]