FROM python

RUN mkdir /opt/uwu_dating
WORKDIR /opt/uwu_dating

COPY src/python/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
