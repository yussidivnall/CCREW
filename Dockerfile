FROM python:3.11.2-slim
RUN mkdir /srv/app
WORKDIR /srv/app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY ./ /srv/app
# Can only work with single worker, don't do "-w 4"
# Need to ensure worker threads (track and alert) only start a single instance
CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:5000"]
