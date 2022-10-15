FROM python:3.9-slim

ENV C_FORCE_ROOT true

ENV HOST 0.0.0.0
ENV PORT 8080
ENV DEBUG true

COPY . /api
WORKDIR /api

RUN pip install -U setuptools pip
RUN pip install -r requirements.txt

EXPOSE 8080

RUN pip install gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "gunicorn --worker-tmp-dir /dev/shm app.py"]