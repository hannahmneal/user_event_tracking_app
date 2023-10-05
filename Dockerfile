FROM python:3

WORKDIR /api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn api.server:app --port 8080 --reload --log-level info"]