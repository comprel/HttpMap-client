import os
import sys
import time
from bin.info import AccessInfo
from bin.report import ReportAccess


def is_correct_line(data):
    return len(data) == 8


def is_access_data(data):
    return data[3] == ">"


def is_report_data(data):
    if data.startswith("-"):
        request_data = data.split()
        if is_correct_line(request_data) and is_access_data(request_data):
            return True


def check_sniffer():
    if not os.path.exists("/usr/local/netmap/access.log"):
        print("请启动sniffer ...")
        sys.exit(1)


def analysis_access():
    check_sniffer()
    thefile = open("/usr/local/netmap/access.log", 'r')
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(1)
            continue
        if is_report_data(line):
            yield line


def access_report(uuid, line):
    request_data = line.split()
    src = request_data[1]
    dest = request_data[2]
    is_local, is_report = AccessInfo.is_flush_local_ips(dest)
    if is_local and is_report:
        status = ReportAccess.report_local(uuid, dest)
        if not status:
            AccessInfo.local_ips.remove(dest)
            AccessInfo.write_local_ips()
    if is_local:
        is_report = AccessInfo.is_report_access_ips(src)
        if is_report:
            status = ReportAccess.report_access(uuid, request_data)
            if not status:
                AccessInfo.access_ips.remove(src)
                AccessInfo.write_access_ips()


def run_report(uuid):
    if not uuid:
        print("未知服务注册信息")
        sys.exit(1)
    for new_line in analysis_access():
        try:
            access_report(uuid=uuid, line=new_line)
        except:
            pass


if __name__ == '__main__':
    run_report(uuid="xx")
