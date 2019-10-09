import urllib
import urllib2
from conf.setting import access_url
from conf.setting import api_service
from conf.setting import localipaddress_url
from lib.logs import logger


class ReportAccess(object):
    @classmethod
    def report_access(cls, uuid, request_data):
        data = {"id": uuid, "src": request_data[1],
                "dest": request_data[2],
                "port": request_data[5],
                "url": request_data[-1]}
        request = urllib2.Request("http://%s" % api_service + access_url)
        request.add_header('content-type', 'application/json')
        response = urllib2.urlopen(request, urllib.urlencode(data), timeout=5)
        logger.info(response.read())
        if response.getcode() == 201:
            return True
        return False

    @classmethod
    def report_local(cls, uuid, ip):
        data = {"host_id": uuid, "ip": ip}
        request = urllib2.Request("http://%s" % api_service + localipaddress_url)
        request.add_header('content-type', 'application/json')
        response = urllib2.urlopen(request, urllib.urlencode(data), timeout=5)
        logger.info(response.read())
        if response.getcode() == 201:
            return True
        return False
