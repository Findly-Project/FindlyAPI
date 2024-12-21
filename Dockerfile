FROM python

WORKDIR /src

COPY poetry.lock pyproject.toml /src
RUN pip install poetry && poetry install

COPY . /src

EXPOSE 5000

CMD ["/bin/bash", "-c", "poetry run python app.py"]