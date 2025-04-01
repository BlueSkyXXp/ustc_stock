#!/bin/sh

# 定义日志文件路径
LOG_FILE="/var/logs/cron/cron_minute.log"

# 创建日志目录（如果不存在）
mkdir -p $(dirname $LOG_FILE)

# 记录开始时间
echo "$(date +%Y-%m-%d:%H:%M:%S) - 开始执行基本数据分钟任务" >> $LOG_FILE

# 执行 Python 脚本，并将输出追加到日志文件



/usr/local/bin/python3 /data/app/job/basic_data_minute_job.py  >> $LOG_FILE 2>&1

# 记录结束时间
echo "$(date +%Y-%m-%d:%H:%M:%S) - 基本数据分钟任务执行结束" >> $LOG_FILE