FROM python:3.13.5-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    && pip install --upgrade pip \
    && pip install poetry && poetry config virtualenvs.create false

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install

COPY . .

EXPOSE 8000

RUN chmod +x ./prestart.sh

ENTRYPOINT [ "./prestart.sh" ]

CMD [ "python", "-m", "src.main" ]