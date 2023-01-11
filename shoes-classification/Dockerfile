FROM python:3.8
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN pip install numpy --upgrade
CMD python app.py
