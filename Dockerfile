# set base image (host OS)
FROM python:latest
# set the working directory in the container# copy the dependencies file to the working directory
COPY . .
# install dependencies
RUN pip install -r requirements.txt
# copy the content of the local src directory to the working directory
# command to run on container start
CMD ["python", "src/main.py"]