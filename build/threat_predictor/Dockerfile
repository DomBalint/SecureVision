ARG SV_REGISTRY
FROM ${SV_REGISTRY}/base_python3_ml:1.0.0

WORKDIR /home/svadm/

COPY system/ ./system/
COPY models/schemas/ ./schemas/
COPY source/svlib/ ./svlib/
COPY source/threat_detection/artifacts/saved_models/ ./saved_models/
COPY source/components/threat_predictor/ .

CMD ["python3", "threat_predictor.py"]