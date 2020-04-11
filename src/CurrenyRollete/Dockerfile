  
FROM python:3-alpine

WORKDIR /app

COPY . /app

EXPOSE 30003

RUN pip install --requirement /app/requirements.txt

CMD ["python","/app/CurrencyRouletteGame.py"]
