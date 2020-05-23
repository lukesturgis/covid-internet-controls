FROM python:latest

HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost:42075/ping || exit 1

COPY ./ /worker

RUN pip install --no-cache-dir -r /worker/requirements.txt

EXPOSE 42075

CMD ["gunicorn", "--chdir", "/worker", "run_worker:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:42075"]