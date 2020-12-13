ARG SV_REGISTRY
FROM ${SV_REGISTRY}/base_backend:1.0.0

WORKDIR /home/svadm

COPY system/ ./system/
COPY source/backend/database/ ./database/
#COPY source/frontend/ ./frontend/
COPY source/frontend/ ./api/templates/
COPY source/svlib/ ./svlib/
COPY source/backend/api/ ./api/

CMD ["python3", "./api/api_class.py"]
