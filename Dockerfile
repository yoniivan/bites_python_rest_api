FROM python

ADD . /airplanes
WORKDIR /airplanes

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV PYTHONUNBUFFERED 1