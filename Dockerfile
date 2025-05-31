FROM python:3.13-alpine AS base

LABEL maintainer=codeBuddha

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    postgresql-dev \
    musl-dev \
    gcc \
    python3-dev \
    libpq


COPY ./requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ONLY BECAUSE THE APP IS NOT FOR PROD
RUN addgroup -S jam && adduser -S jam -G jam \
    && chown -R jam:jam /app \
    && chmod -R 777 /app

USER jam


FROM base AS development
COPY . .
EXPOSE 7000
CMD ["uvicorn", "app.index:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
