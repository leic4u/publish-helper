FROM python:3.11.4-slim-bullseye
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ENV API_PORT="15372" \
    NGINX_PORT="15373" \
    UMASK=000
WORKDIR "/app"
COPY lib_deb lib_deb
COPY src src
COPY static static
COPY temp temp
COPY docs/requirements_api.txt requirements_api.txt
RUN mkdir media  \
    && apt-get update -o Acquire::Check-Valid-Until=false  \
    && apt-get install -y libmediainfo0v5 libzen0v5 nginx gettext-base  \
    && cp -r lib_deb/entrypoint entrypoint \
    && chmod +x entrypoint \
    && cp -r lib_deb/nginx.conf /etc/nginx/nginx.template.conf\
    && pip install -r requirements_api.txt --trusted-host mirrors.aliyun.com --default-timeout=600 -i https://mirrors.aliyun.com/pypi/simple/
USER root
EXPOSE 15372 15373
ENV PYTHONPATH=${PYTHONPATH}:.
CMD ["sh", "entrypoint"]
