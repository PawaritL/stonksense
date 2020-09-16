FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
# copy the dependencies file to the working directory
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app /app/app