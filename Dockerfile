FROM python:3.12-slim

WORKDIR /usr/src

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

RUN poetry install --only main

COPY . .

RUN . /usr/src/.venv/bin/activate
CMD ["python", "main.py"]
