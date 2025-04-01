FROM python:3.10-bullseye
LABEL authors="bytedance"

#增加语言utf-8
ENV LANG=zh_CN.UTF-8
ENV LC_CTYPE=zh_CN.UTF-8
ENV LC_ALL=C

WORKDIR /data

RUN sed -i "s@http://\(deb\|security\).debian.org@https://mirrors.aliyun.com@g" /etc/apt/sources.list

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

RUN apt-get update && apt-get install -y cron && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /data/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app /data/app
COPY supervisor /data/supervisor
COPY bin /data/bin
COPY cron/cron.minutely /etc/cron.minutely
COPY cron/cron.night /etc/cron.night
COPY cron/cron.hourly /etc/cron.hourly
COPY cron/cron.workdayly /etc/cron.workdayly
COPY cron/cron.monthly /etc/cron.monthly
EXPOSE 8000

RUN mkdir -p /var/spool/cron/crontabs
RUN mkdir -p /var/log/cron && chmod 777 /var/log/cron

RUN chmod 755 /data/bin/run_*.sh && \
    chmod 755 /etc/cron.hourly/* && \
    chmod 755 /etc/cron.workdayly/* && \
    chmod 755 /etc/cron.monthly/* && \
    chmod 755 /etc/cron.minutely/* && \
    chmod 755 /etc/cron.night/* && \
    chmod 755 /data/app && \
    echo "SHELL=/bin/sh \n\
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin \n\
# min hour day month weekday command \n\
*/15 9,10,11,13,14,15 * * 1-5 /bin/run-parts /etc/cron.minutely >> /var/log/cron/cron_minutely.log 2>&1 \n\
0 23 * * 1-5 /bin/run-parts /etc/cron.night >> /var/log/cron/cron_night.log 2>&1 \n\
*/30 9,10,11,13,14,15 * * 1-5 /bin/run-parts /etc/cron.hourly >> /var/log/cron/cron_hourly.log 2>&1 \n\
30 17 * * 1-5 /bin/run-parts /etc/cron.workdayly >> /var/log/cron/cron_workdayly.log 2>&1 \n\
30 10 * * 3,6 /bin/run-parts /etc/cron.monthly \n" > /var/spool/cron/crontabs/root && \
    chmod 600 /var/spool/cron/crontabs/root

ENTRYPOINT ["supervisord","-n","-c","/data/supervisor/supervisord.conf"]