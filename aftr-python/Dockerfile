FROM python:3.11-slim

# Sample so that we aren't running as root
RUN useradd -ms /bin/bash supercooldev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x startup_db.py

USER supercooldev

CMD ["python", "startup_db.py", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
