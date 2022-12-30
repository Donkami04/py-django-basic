FROM python:3.10

ENV PYTHONUNBUFFERED 1

# RUN apk update \
#     && apk add --virtual build-deps gcc python3-dev musl-dev \
#     && apk add postgresql-dev \
#     && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
#     && apk add libffi-dev py-cffi \
#     && apk add gettext \
#     && apk add postgresql-client

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]

