FROM aexea/aexea-base
MAINTAINER Stuttgart Python Interest Group

EXPOSE 8012

USER root
RUN curl -sL https://deb.nodesource.com/setup_5.x | bash -
RUN apt-get update && apt-get install -y ttf-dejavu-core nodejs
RUN easy_install3 -U pip

# install uwsgi for production
RUN pip3 install uwsgi

WORKDIR /opt/code/cress
ADD cress/package.json /opt/code/cress/package.json
RUN npm install

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
