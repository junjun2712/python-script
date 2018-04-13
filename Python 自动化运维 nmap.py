import sys
import nmap

scan_row = []    
input_data = raw_input("PLEASE INPUT: ")
scan_row = input_data.split(" ")
if len(scan_row) != 2:
    print ("error")
    sys.exit(0)
hosts = scan_row[0]  ##输入的主机
port = scan_row[1]   ##输入的端口

try:
    nm = nmap.PortScanner()  ##实例化扫描对象
except nmap.PortScannerError:    
    print ("Nmap not",sys.exc_info()[0])
    sys.exit(0)
except:
    print ("unexpecterd Error:",sys.exc_info()[0])
    sys.exit(0)


try:
    nm.scan(hosts=hosts , arguments='-v -sS -p' + port )  ##指定扫描主机和参数
except Exception,e:
    print "scan error: " + str(e)
for host in nm.all_hosts():
    print ('--------------------------------------')
    print ('Host : %s (%s)' %(host,nm[host].hostname()))   ##输出主机名 
    print ('State : %s' % nm[host].state())  ##输出主机状态
    for proto in nm[host].all_protocols():  ##遍历协议
        print ('---------')
        print ('Protocil : %s' %proto )  ##输出协议名

        lport = nm[host][proto].keys()  ##获取所有扫描端口
        lport.sort()  ##对端口排序
        for port in lport:   ##遍历端口和装态
            print ('port : %s\tstate : %s' %(port,nm[host][proto][port]['state']))