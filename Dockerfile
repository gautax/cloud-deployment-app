# Example Dockerfile for Streamlit
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Start Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
