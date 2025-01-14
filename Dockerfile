FROM python:3.10


# RUN apt-get update
# RUN apt-get install -y git

WORKDIR /app
COPY . /app


RUN pip install -r req.txt



EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "app/core/log.config"]
