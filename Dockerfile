FROM python

WORKDIR /usr/src/FindlyAPI

COPY poetry.lock pyproject.toml ./
RUN pip install poetry && poetry install

COPY . .

CMD ["/bin/bash", "-c", "poetry run python app.py"]