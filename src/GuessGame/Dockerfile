  
FROM python:3-alpine

WORKDIR /app

COPY . /app

EXPOSE 30002

RUN pip install --requirement /app/requirements.txt

CMD ["python","/app/GuessGame.py"]
