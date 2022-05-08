FROM python:3.10

WORKDIR /app

COPY ./requirements.txt ./

RUN python3 -m pip install -r ./requirements.txt

COPY ./src ./

CMD ["uvicorn", "--host", "0.0.0.0", "--reload", "backend:app"]