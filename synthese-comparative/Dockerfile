# Dockerfile for SyntheseComparative microservice

FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure stdout/stderr are unbuffered
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system deps (optional, adjust if you need more)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app

# Expose port
EXPOSE 8005

# Env defaults (FAKE mode by default; override in docker-compose for REAL)
ENV USE_FAKE_RETRIEVAL=true
ENV USE_FAKE_LLM=true
ENV SEMANTIC_INDEXER_URL=http://semantic-indexer:8003
ENV LLM_QA_URL=http://llm-qa:8004

# Start the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
