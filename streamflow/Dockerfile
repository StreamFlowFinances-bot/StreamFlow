FROM python:3.10-slim
WORKDIR /app
RUN pip install nicegui pandas
COPY . .
EXPOSE 10000
CMD ["python", "main.py"]
