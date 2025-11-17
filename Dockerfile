FROM python:3.11-slim

# Install system dependencies (Cairo)
RUN apt-get update && \
    apt-get install -y libcairo2-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY 0.0.a_requirements_intent_manifest.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r 0.0.a_requirements_intent_manifest.txt

# Copy all application code
COPY . .

# Expose port (Render will map this)
EXPOSE 5000

# Run the server
CMD ["python", "server_main.py"]
