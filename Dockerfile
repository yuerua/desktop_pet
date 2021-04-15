FROM python:3.7


ENV DISPLAY :0
CMD export DISPLAY =":0"

COPY requirements.txt ./
#RUN apk update &&  apk add --upgrade --no-cache \
#	libpq uwsgi-python3 \
#	py3-pip alpine-sdk postgresql-dev postgresql \
#        bash openssh curl ca-certificates openssl less htop \
#	g++ make wget rsync \
#        build-base libpng-dev freetype-dev libexecinfo-dev openblas-dev libgomp lapack-dev \
#        libgcc libquadmath musl  \
#	libgfortran \
#	lapack-dev \
#	libxml2 \
#	libxslt \
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . ./app
WORKDIR ./app

CMD [ "python", "./main_shiori.py" ]
