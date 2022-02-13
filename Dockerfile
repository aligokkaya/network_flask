FROM debian:latest


RUN apt-get update && apt-get install -y apache2 \
    ssmtp\
    openssl\
    mailutils \
    libapache2-mod-wsgi-py3 \
    build-essential \
    python3 \
    python3-pip \
    python3-git \
    python3-dev\
    vim \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*


RUN set -eux; \
        apt-get update; \
        apt-get install -y --no-install-recommends gcc; \
    apt-get install -y libleptonica-dev; \
    apt-get install -y ca-certificates ;\
	apt-get install -y libevent-dev; \
    apt-get install -y poppler-utils; \
        apt-get -y  autoremove gcc; \
        rm -rf /var/lib/apt/lists/*
 
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		libgl1-mesa-glx \
		ffmpeg \
	; \
	rm -rf /var/lib/apt/lists/*

RUN apt-get update -y

# RUN apt-get install -y gir1.2-gobject-2.0 
# RUN apt-get update -y
RUN apt-get install -y libpango-1.0-0
RUN apt-get install -y libpangoft2-1.0-0


# Copy over and install the requirements
COPY ./app/requirements.txt /var/www/apache-flask/app/requirements.txt

RUN pip install -r /var/www/apache-flask/app/requirements.txt

# RUN pip install https://github.com/JustAnotherArchivist/snscrape
# Copy over the apache configuration file and enable the site

# COPY myCA.pem  /usr/local/share/ca-certificates/myCA.crt

# RUN apt-get update -y


COPY server.crt /etc/apache2/ssl/server.crt
COPY server.key /etc/apache2/ssl/server.key
COPY privkey.pem /etc/apache2/ssl/privkey.pem
# COPY inster-ca.crt /etc/apache2/ssl/inter-ca.crt


COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf
RUN a2ensite apache-flask
RUN a2enmod headers
RUN a2enmod ssl
# Copy over the wsgi file
COPY ./apache-flask.wsgi /var/www/apache-flask/apache-flask.wsgi

COPY ./run.py /var/www/apache-flask/run.py
COPY ./app /var/www/apache-flask/app/



RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf

# LINK apache config to docker logs.
RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
    ln -sf /proc/self/fd/1 /var/log/apache2/error.log


# RUN mv /var/www/apache-flask/app/snscrape /var/www/apache-flask/
EXPOSE 80
RUN echo -e "$(hostname -i)\t$(hostname) $(hostname).localhost" >> /etc/hosts
WORKDIR /var/www/apache-flask
RUN ["chown", "-R", "www-data:www-data", "/var/www"]

CMD  /usr/sbin/apache2ctl -D FOREGROUND

