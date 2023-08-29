FROM python:3.8

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
RUN echo "Using API key: $OPENAI_API_KEY"

COPY requirements.txt ./requirements.txt
COPY utils.py ./utils.py
COPY main.py ./main.py

RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

CMD ["python", "./main.py"]