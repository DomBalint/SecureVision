ARG SV_REGISTRY
FROM ${SV_REGISTRY}/base_python3:1.0.0

WORKDIR /home/svadm/

COPY system/ ./system
COPY models/schemas/ ./schemas
COPY source/svlib/ ./svlib
COPY source/components/simulator/ .

CMD ["python3", "simulator.py"]