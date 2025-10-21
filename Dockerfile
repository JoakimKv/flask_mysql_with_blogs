# Use a lightweight Python base
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libssl-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /flask_mysql_with_blogs_docker

# Copy dependency list and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY . .

# Expose the port Flask/Gunicorn will run on
EXPOSE 5000

# Run with Gunicorn (Flask app factory pattern)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flaskr_carved_rock:create_app()"]

# Copy entrypoint and make executable
COPY docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

# Run entrypoint (collectstatic + gunicorn)
ENTRYPOINT ["./docker-entrypoint.sh"]

