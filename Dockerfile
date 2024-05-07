FROM python:3.11-alpine

WORKDIR /app
COPY . .
RUN apk add --no-cache rust cargo
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
