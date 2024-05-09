FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libmagic-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY config.yml ./

COPY *.py ./

COPY prod_keys/computacionubicuaalvaroseoane-firebase-adminsdk-bvofg-c0f4c62bb0.json prod_keys/firebaseConfig.json ./

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "entrypoint.py", "config.yml"]