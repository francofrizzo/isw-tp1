FROM alpine:latest

RUN echo '@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing' >>/etc/apk/repositories
RUN apk update
RUN apk add \
    gcc musl musl-dev make \
    git openssh mksh \
    postgresql-dev sqlite sqlite-libs sqlite-dev \
    geos-dev@testing proj4-dev@testing libxml2-dev \
    python3 python3-dev \
    vim
RUN python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /root/.cache
RUN pip install virtualenv

WORKDIR /tmp
RUN wget -O - 'http://www.gaia-gis.it/gaia-sins/libspatialite-4.3.0a.tar.gz' | tar -xzf -
WORKDIR /tmp/libspatialite-4.3.0a
RUN ./configure --disable-freexl && make -j && make install
WORKDIR ..
RUN rm -rf libspatialite-4.3.0a

RUN adduser -s /bin/mksh -D admin
ADD ssh/ /home/admin/.ssh
RUN chown -R admin:admin /home/admin/.ssh
RUN chmod 700 /home/admin/.ssh

USER admin
ENV HOME /home/admin
WORKDIR ${HOME}
RUN git clone git@github.com:francofrizzo/isw-tp1
WORKDIR ${HOME}/isw-tp1
RUN virtualenv wifindbar \
    && source wifindbar/bin/activate \
    && pip install -U -r requirements.txt \
    && ./manage.py migrate
EXPOSE 8000
ENTRYPOINT /bin/mksh
