FROM dckr/docker-backup
MAINTAINER Johannes 'fish' Ziemke <fish@docker.com>

RUN \
  apk update && \
  apk upgrade && \
  apk add git python py-setuptools py-dateutil && \
  git clone https://github.com/s3tools/s3cmd.git /s3cmd && \
  cd /s3cmd && python setup.py install

ADD run   /docker-backup/
ADD s3cfg /.s3cfg
ENTRYPOINT [ "./run" ]
