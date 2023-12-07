FROM python:3.7.17-alpine3.18

RUN apk upgrade --update-cache --available && \
    apk add openssl \
            python3-dev \
            gcc \
            libc-dev \
            libffi-dev \
            libressl-dev && \
    rm -rf /var/cache/apk/*

WORKDIR /home/cp

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app/__init__.py app/__init__.py
COPY app/common/ app/common/
COPY app/peggy/ app/peggy/

# Create an appuser
RUN addgroup --system --gid 10010 appgroup
RUN adduser --system --no-create-home -G appgroup --uid 10010 appuser
RUN chown -R appuser:appgroup /home
USER appuser

EXPOSE 8080

CMD ["tail", "-f", "/dev/null"]
