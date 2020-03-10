FROM python:3-alpine

RUN adduser -D -s /bin/nologin aha

WORKDIR /trufflemog

USER aha

ADD --chown=aha:aha requirements.txt .

RUN pip install --user -r requirements.txt

ENV PATH $PATH:/home/aha/.local/bin

ADD --chown=aha:aha . .

CMD python3 run.py
