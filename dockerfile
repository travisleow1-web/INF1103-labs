FROM python:3.11-slim
WORKDIR /usr/src/app
COPY smart_auditor.py .
CMD ["python", "smart_auditor.py"]