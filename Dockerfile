FROM    python:3.9-slim-buster AS base
ENV     PYTHONUNBUFFERED True
WORKDIR /src
RUN     apt update && \
        pip install pipenv

FROM    base AS builder
COPY    *.py *.yaml Pipfile*  ./
ADD     data/* data/
ADD     modules/* modules/
RUN     mkdir ai-models && \
        pipenv install --system --deploy && \
        python -m modules.matcher

CMD     uvicorn main:app --host 0.0.0.0 --port $PORT
# CMD     gunicorn --bind 0.0.0.0:$PORT -w 4 -k uvicorn.workers.UvicornWorker main:app 