FROM python:3.11-slim
WORKDIR /usr/src/app
COPY inventory_auditor.py .
CMD ["python", "inventory_auditor.py"]