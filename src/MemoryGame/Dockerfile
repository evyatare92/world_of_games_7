  
FROM python:3-alpine

WORKDIR /app

COPy . /app

EXPOSE 80

RUN pip install --requirement /app/requirements.txt

CMD ["python","/app/MemoryGame.py"]
