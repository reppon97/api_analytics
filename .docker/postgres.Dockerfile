FROM postgres:13
COPY .docker/init.sql /docker-entrypoint-initdb.d/
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8