# Note: Image could be changed to Debian Bullseye for future dependency changes
FROM python:3.10.0-alpine3.15
COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt && rm requirements.txt
COPY . /
ENTRYPOINT ["python", "/sbom.py"]
