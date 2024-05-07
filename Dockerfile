FROM python:3.12-alpine

WORKDIR /app
COPY main.py nut_client.py utils.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
