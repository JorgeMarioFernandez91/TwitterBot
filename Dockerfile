#install ubuntu in container and copy python script into it
FROM ubuntu:18.04
COPY script.py .
COPY setup.sh . 

#update ubuntu and instaill pip3
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && pip3 install --upgrade pip \
  && pip --version

#install beautifulsoup
RUN apt-get install -y python3-bs4 \
  && pip3.6 install beautifulsoup4 \
  && pip install requests

#install ruby and twitter api
RUN apt install ruby-full -y
RUN gem install twurl

#run command for program
#CMD ["python3", "script.py"]
CMD ["./setup.sh"]