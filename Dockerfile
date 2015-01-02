FROM dckr/docker-backup
MAINTAINER Johannes 'fish' Ziemke <fish@docker.com>

RUN apt-get update && apt-get -y -q install python-setuptools python-dateutil python-magic
RUN git clone https://github.com/s3tools/s3cmd.git /s3cmd
RUN cd /s3cmd && python setup.py install

ADD run   /docker-backup/
ADD s3cfg /.s3cfg
ENTRYPOINT [ "./run" ]
