FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
COPY .env .
EXPOSE 8080

# Run script when the container launches
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
