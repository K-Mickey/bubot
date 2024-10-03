FROM python:3.12-slim

WORKDIR /usr/src

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

RUN poetry install --only main

COPY . .

CMD ["poetry", "run", "python", "/usr/src/main.py"]
