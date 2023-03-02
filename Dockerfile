FROM python:alpine
COPY app.py requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]