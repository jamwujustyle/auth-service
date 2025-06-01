FROM python:3.13-alpine AS base

LABEL maintainer=codeBuddha

WORKDIR /auth-service

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    postgresql-dev \
    musl-dev \
    gcc \
    python3-dev \
    libpq


COPY ./requirements.txt /auth-service

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ONLY BECAUSE THE APP IS NOT FOR PROD
RUN addgroup -S jam && adduser -S jam -G jam


FROM base AS development
COPY . /auth-service

RUN chown -R jam:jam /auth-service \
    && chmod -R 755 /auth-service

USER jam

EXPOSE 1000
CMD ["uvicorn", "app.index:app", "--host", "0.0.0.0", "--port", "1000", "--reload"]
