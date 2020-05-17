ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

ENV ROOT_DIR /data

# Install packages
RUN apt-get -qq update
RUN apt-get install -yqq python3 python3-dev python3-pip
RUN pip3 install --quiet --upgrade pip

COPY requirements.txt /
RUN pip3 install -r requirements.txt

# Copy files for add-on
COPY run.sh main.py errors.py /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]