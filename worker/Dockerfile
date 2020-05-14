FROM python:latest

COPY ./ /worker

RUN pip install --no-cache-dir -r /worker/requirements.txt

EXPOSE 42075

CMD ["gunicorn", "--chdir", "/worker", "main:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:42075"]