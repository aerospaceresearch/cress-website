FROM python:3.6
MAINTAINER cress.space Team

EXPOSE 8012

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    bash \
    curl \
    g++ \
    git \
    lib32z1-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libmemcached-dev \
    locales \
    postgresql-client \
    postgresql-server-dev-all \
    zlib1g-dev \
    ttf-dejavu-core libpq-dev \
    && rm -rf /var/lib/apt/lists/*


ADD requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip install --find-links=http://pypi.qax.io/wheels/ --trusted-host pypi.qax.io -Ur requirements.txt
ADD . /opt/code

# user
RUN useradd uid1000 -d /home/uid1000
RUN mkdir -p /home/uid1000 && chown uid1000: /home/uid1000
VOLUME /home/uid1000

RUN chown -R uid1000: /opt

USER uid1000

WORKDIR /opt/code/cress

# production stuff
ENTRYPOINT ["./start.sh"]
CMD ["web"]
