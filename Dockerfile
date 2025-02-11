FROM python:3.9
WORKDIR /app
COPY vp_alert.py config.json ./
RUN pip install requests
CMD ["python", "vp_alert.py"]
