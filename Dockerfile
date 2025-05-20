FROM python:3.13

WORKDIR /app

COPY requirements.txt .

# Force upgrade pip + print installation output
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip list

COPY . .

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
