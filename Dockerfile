FROM python:3.7-stretch
RUN mkdir /code
RUN mkdir /mnt/shared-volume/media
RUN mkdir /mnt/shared-volume/static
RUN apt-get install -y gcc libmariadb-devel redis-server
RUN service redis-server start
WORKDIR /code
ADD requirements-production.txt /code/
RUN pip install -r requirements-production.txt
ADD . /code/

ENTRYPOINT ["sh","/code/run_akkaskhoone.sh"]