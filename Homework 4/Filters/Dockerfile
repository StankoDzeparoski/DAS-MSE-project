FROM python:3.10-slim
WORKDIR /Filters
COPY . /Filters/
COPY requirements.txt /Filters/
RUN pip install --no-cache-dir -r requirements.txt
#the microservice will run on
EXPOSE 5000
#the filter service
CMD ["python", "main.py"]