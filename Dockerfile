FROM python:3.9.13

COPY Pipfile      /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv sync --system --dev

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]