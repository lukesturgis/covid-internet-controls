FROM python:latest

ENV BIND_PORT 42075

COPY ./ /

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $BIND_PORT

CMD ["python", "./run_worker.py"]