FROM python:3.12.3-slim

RUN pip install poetry==2.1.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY . /app/

RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "portfolio_trajectory.main:app", "--host", "0.0.0.0", "--port", "8000"]