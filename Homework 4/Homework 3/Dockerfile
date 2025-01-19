FROM python:3.9-slim
WORKDIR /Homework\ 3
COPY . /Homework\ 3/
COPY requirements.txt /Homework\ 3/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "fundamental_analysis.py"]
