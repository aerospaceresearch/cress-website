FROM aexea/aexea-base:py3.5
MAINTAINER Stuttgart Python Interest Group

EXPOSE 8012

USER root
RUN apt-get update && apt-get install -y ttf-dejavu-core libpq-dev python3-dev
RUN easy_install3 -U pip

# install uwsgi for production
RUN pip3 install uwsgi

ADD requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip3 install --find-links=http://pypi.qax.io/wheels/ --trusted-host pypi.qax.io -Ur requirements.txt
ADD . /opt/code

RUN chown -R uid1000: /opt

WORKDIR /opt/code/cress

# uid1000 is created in aexea-base
USER uid1000

# production stuff
ENTRYPOINT ["./start.sh"]
CMD ["web"]
