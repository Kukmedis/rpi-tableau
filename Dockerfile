FROM python:3

ADD main.py main.py
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["main.py"]