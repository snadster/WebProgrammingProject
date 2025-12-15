# Use an official Python runtime as a parent image
FROM python:slim

# copy requirements and install them
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy application
COPY . ./

# Flask config
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# expose Flask’s port
EXPOSE 5000

# run Flask App
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
