#!/bin/bash


# 本脚本适用于日本机房VM新增磁盘LVM使用


test $# -ne 1 && { echo -e "\n\033[36mUsage: $0 disk[/dev/sdb]:要做lv的磁盘\n\033[0m"; exit 1; }
test -d /data || mkdir /data

DISK_NAME="$1"
# 检测系统是否已识别新磁盘，如未检测到退出
fdisk -l $DISK_NAME &>/dev/null || \
{ echo -e "\n\033[33m没找到 ${DISK_NAME} 磁盘,请检查!\n\033[0m"; exit; }


# 检测磁盘是否是新磁盘（是否有做分区），如已有分区退出
grep -qE "Start.*End.*Blocks" <<<$(fdisk -l $DISK_NAME) && \
{ echo -e "\n\033[33m磁盘:$DISK_NAME 已做分区，请确认是否是新挂载磁盘!\n\033[0m"; exit 1; }

# 检测磁盘是否是已做pv, 如已做pv退出
grep -qE " $DISK_NAME " <<<$(pvs) && \
{ echo -e "\n\033[33m磁盘:$DISK_NAME 已做PV，请确认是否是新挂载磁盘!\n\033[0m"; exit 1; }


echo -e "\n\033[36m  >>> 开始创建PV逻辑卷 ..\033[0m"
pvcreate $DISK_NAME
test $? -eq 0 || { echo -e "\n\033[31m 创建PV失败!\n"; exit 1; }
pvs

echo -e "\n\033[36m  >>> 将PV加入VG centos ..\033[0m"
vgextend centos $DISK_NAME
test $? -eq 0 || { echo -e "\n\033[31m 加入VG失败!\n"; exit 1; }
vgs

echo -e "\n\033[36m  >>> 创建LV data ..\033[0m"
lvcreate -l 100%FREE -n data centos
test $? -eq 0 || { echo -e "\n\033[31m 创建LV失败!\n"; exit 1; }
lvs

echo -e "\n\033[36m  >>> 格式化LV /dev/centos/data ..\033[0m"
mkfs.xfs /dev/centos/data
test $? -eq 0 || { echo -e "\n\033[31m 格式化LV失败!\n"; exit 1; }

echo -e "\n\033[36m  >>> 挂载LV，并设置磁盘开机自动挂载..\033[0m"
echo "/dev/centos/data /data xfs defaults 0 0" >> /etc/fstab
mount -a
test $? -eq 0 || { echo -e "\n\033[31m LV挂载失败!\n"; exit 1; }
df -h | grep /data


echo -e "\n\033[32mlvm逻辑卷已经创建完成,请检查确认, 确认无误后重启服务器\n\033[0m"
