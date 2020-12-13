ARG SV_REGISTRY
FROM ${SV_REGISTRY}/base_backend:1.0.0

WORKDIR /home/svadm

COPY source/backend/database/ .
COPY system/ ./system/
COPY source/svlib ./svlib/

CMD ["python3", "db_handler_kafka.py"]
