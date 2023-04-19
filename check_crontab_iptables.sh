#!/bin/bash

#此脚本用于检测linux系统重要文件是否被改动

#建议用定时任务执行此脚本，如每5分钟执行一次，也可修改此脚本用于死循环检测

#Ver:1.0

#定义验证文件所在目录

FileDir='/var/CheckFile'

#获取主机名或自己定义

HostName=$(hostname)

#生产iptables配置文件
/sbin/iptables-save > /etc/sysconfig/iptables

#定义需要验证的文件目录，/etc一般是系统重要的配置文件，其它重要的文件，如网站程序文件等，也可以添加到以下数组中，每个目录为一行，根据自己情况添加吧

CheckDir=(

/etc/
/var/spool/cron/

)

#生成所定义需验证的文件样本日志函数

OldFile () {

for i in ${CheckDir[@]}

do

/bin/find ${i} -type f |xargs md5sum >> ${FileDir}/old.log

done

}

#生成所定义文件新日志函数

NewFile () {

for i in ${CheckDir[@]}

do

/bin/find ${i} -type f |xargs md5sum >> ${FileDir}/new.log

done

}

#假如验证文件目录不存在则创建

if [ ! -d ${FileDir} ]

then

mkdir ${FileDir}

fi

#假如样本日志不存在则创建

if [ ! -f ${FileDir}/old.log ]

then

OldFile

fi



#生成新验证日志

NewFile

#新验证日志与样本日志进行比较

/usr/bin/diff ${FileDir}/new.log ${FileDir}/old.log >${FileDir}/diff.log

Status=$?

#假如比较结果有变化，则发送邮件报警

if [ ${Status} -ne 0 ]

then

echo "$(hostname) crontab diff" >> /var/log/tcpwrap_deny.log
fi

#清除新旧日志，把比较结果进行备份

/bin/mv -f ${FileDir}/diff.log ${FileDir}/diff$(date +%F__%T).log

cat /dev/null > ${FileDir}/old.log

cat /dev/null > ${FileDir}/new.log


#重新生成样本日志

OldFile

#删除目录内30天以前的比较结果备份文件

/bin/find ${FileDir} -type f -mtime +30 |xargs rm -f
