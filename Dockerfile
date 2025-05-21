FROM python:3.13

# Set working directory
WORKDIR /app

# Set Hugging Face cache path (used in fuzzy_search.py)
ENV HF_HOME=/app/model_cache
ENV TRANSFORMERS_CACHE=/app/model_cache

# Install only what's needed first (enables layer caching)
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your app
COPY . .

# Run FastAPI app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
