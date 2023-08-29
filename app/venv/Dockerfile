FROM python:3.8

COPY requirements.txt ./requirements.txt
COPY utils.py ./utils.py
COPY main.py ./main.py

RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

CMD ["python", "./main.py"]