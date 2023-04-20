FROM python
WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY . .
RUN mkdir /data/
CMD [ "python","-u", "./aurora_receiver.py" ]