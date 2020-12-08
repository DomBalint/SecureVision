FROM ubuntu:18.04

ENV TZ=Europe/Budapest

RUN \
    # sysadmin settings
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    \
    # install some sysadmin stuff
    apt-get update && \
    apt-get install -y vim mc less tzdata && \
    apt-get install -y telnet && \
    apt-get install -y git && \
    \
    # install python stuff
    apt-get install -y python3 python3-pip && \
    pip3 install pyyaml && \
    pip3 install jsonschema && \
    pip3 install apscheduler && \
    pip3 install requests && \
    pip3 install confluent-kafka==1.5.0 && \
    pip3 install python-dateutil

WORKDIR /home/svadm