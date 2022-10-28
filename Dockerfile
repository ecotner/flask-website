FROM python:3.7-slim

WORKDIR /app
RUN apt update && \
    apt install -y \
    default-libmysqlclient-dev \
    gcc
RUN pip install --upgrade pip && \
    pip install poetry==1.2.2 && \
    poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install
COPY . .
ENTRYPOINT [ "flask", "run", "--host", "0.0.0.0", "--port", "4000" ]
