  
FROM python:3-alpine

WORKDIR /app

COPY . /app

EXPOSE 80

RUN pip install --requirement /app/requirements.txt

CMD ["python","/app/MainGame.py"]
