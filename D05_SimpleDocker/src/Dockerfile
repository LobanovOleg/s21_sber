FROM nginx
WORKDIR /src/
ARG USERNAME=nginx

USER root
COPY ./server/nginx.conf /etc/$USERNAME/nginx.conf
COPY ./server/main.c /src/main.c
COPY ./part4/start.sh /src/start.sh
RUN apt-get update; \
    apt-get install -y gcc spawn-fcgi libfcgi-dev; \
    apt-get clean ; \
    rm -rf /var/lib/apt/lists/* ;

RUN chmod 777 start.sh ; \
    gcc main.c -lfcgi -o main ; \
    chmod 777 server ; \
    chmod 755 /bin/su; \
    chmod 755 /usr/bin/chfn; \
    chmod 755 /usr/bin/chsh; \
    chmod 755 /usr/bin/mount; \
    chmod 755 /usr/bin/expiry; \
    chmod 755 /usr/bin/newgrp; \
    chmod 755 /usr/bin/chage; \
    chmod 755 /usr/bin/umount; \
    chmod 755 /usr/bin/passwd; \
    chmod 755 /usr/bin/wall; \
    chmod 755 /usr/bin/gpasswd; \
    chmod 755 /usr/sbin/unix_chkpwd; \
    touch /var/run/nginx.pid; \
    chown -R $USERNAME:$USERNAME /var/run/nginx.pid; \
    chown -R $USERNAME:$USERNAME /var/log/nginx; \
    chown -R $USERNAME:$USERNAME /var/cache/nginx

USER $USERNAME

HEALTHCHECK --interval=10s --timeout=30s --start-period=5s --retries=3 CMD curl -sS 127.0.0.1 || exit 1
ENTRYPOINT [ "sh", "./start.sh" ]