https://dfcx-stte-example-63ietzwyxq-uk.a.run.app

docker run -it --rm gcr.io/holy-diver-297719/dfcx-stte-example /bin/bash

gunicorn --bind 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornWorker main:app 

uvicorn main:app --host 0.0.0.0 --port 8081