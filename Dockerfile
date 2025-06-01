FROM python:3.13-slim AS base

LABEL maintainer=codeBuddha

WORKDIR /auth-service

RUN apt update && apt install -y \
    build-essential \
    libffi-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /auth-service

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ONLY BECAUSE THE APP IS NOT FOR PROD
RUN adduser --disabled-password --no-create-home --gecos "" jam


FROM base AS development
COPY . /auth-service

RUN chown -R jam /auth-service \
    && chmod -R 755 /auth-service

USER jam

EXPOSE 1000
CMD ["uvicorn", "app.index:app", "--host", "0.0.0.0", "--port", "1000", "--reload"]
