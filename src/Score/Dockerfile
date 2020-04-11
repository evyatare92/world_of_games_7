  
FROM python:3-alpine

WORKDIR /app

COPY . /app

EXPOSE 30004

RUN pip install --requirement /app/requirements.txt

CMD ["python","/app/MainScores.py"]
