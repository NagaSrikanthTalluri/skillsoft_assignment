FROM python:3.7-alpine
RUN addgroup -S skillsoft && adduser -S skillsoft -G skillsoft
COPY . /app
WORKDIR /app 
RUN chown -R skillsoft:skillsoft /app
RUN pip install -r requirements.txt
USER skillsoft
CMD ["python3", "app.py"]

