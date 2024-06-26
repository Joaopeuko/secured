FROM python:3.12-slim

RUN pip install --no-cache-dir \
    poetry

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --with dev
