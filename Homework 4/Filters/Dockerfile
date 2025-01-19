FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#the microservice will run on
EXPOSE 5001
#the filter service
CMD ["python", "main.py"]