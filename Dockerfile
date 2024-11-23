FROM python:3.13-slim-bookworm

COPY backend /app

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

CMD ["waitress-serve", "--host", "0.0.0.0", "web:app"]
