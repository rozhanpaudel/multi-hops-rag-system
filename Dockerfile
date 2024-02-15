FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir pipenv
RUN pip install --no-cache-dir -r requirements.txt
COPY .env /app
EXPOSE 8080

# Run script when the container launches
CMD ["pipenv","run","start_api"]
