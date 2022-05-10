FROM python:3.10

WORKDIR /app

COPY ./requirements.txt .

RUN python3 -m pip install -r ./requirements.txt

COPY ./src/import_script.py .

CMD ["python3", "import_script.py"]