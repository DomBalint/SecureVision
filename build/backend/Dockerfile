ARG SV_REGISTRY
FROM ${SV_REGISTRY}/base_python3:1.0.0

RUN \
    apt-get update && \
    apt-get install python3.7.2 && \
    \
    pip3 install SQLAlchemy==1.3.18 && \
    pip3 install dependency-injector && \
    pip3 install Flask==1.1.2 && \
    pip3 install Flask-RESTful==0.3.8 && \
    pip3 install Flask-SQLAlchemy==2.4.3 && \
    pip3 install Flask-Cors==1.10.3 && \
    pip3 install Werkzeug==1.0.1 && \
    pip3 install PyJWT==1.7.1 && \
    pip3 install psycopg2-binary==2.8.6

WORKDIR /home/svadm

COPY . .

CMD ["python3", "backend/api/api_class.py"]
