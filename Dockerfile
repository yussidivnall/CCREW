FROM python:latest
RUN mkdir /srv/app
WORKDIR /srv/app/
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY utils /srv/app/utils/
# COPY run.sh discord_send.py dtypes.py track.py alert.py config.py dash_app.py /srv/app/
COPY ./ /srv/app/
RUN mkdir data
CMD ["./run.sh"]
