import os
import sys
import urllib
import urllib2
from conf.setting import api_service
from conf.setting import register_url
from lib.logs import logger


def __write_register(uuid):
    with open("/usr/local/netmap/.register.info", "w") as f:
        f.write(uuid)
        f.flush()


def __remove_register():
    os.remove("/usr/local/netmap/.register.info")
    os.remove("/usr/local/netmap/.info/access")
    os.remove("/usr/local/netmap/.info/local")


def __check_register(uuid):
    if os.path.exists("/usr/local/netmap/.register.info"):
        with open("/usr/local/netmap/.register.info", "r") as f:
            lines = f.readlines()
            _uuid = lines[0]
            _uuid = _uuid.strip("\n")
            if _uuid == uuid:
                return True
            else:
                logger.info("OLD ID: %s, NEW ID:%s, clear cache info" % (_uuid, uuid))
                __remove_register()
    return False


def register(uuid):
    status = __check_register(uuid)
    if status:
        print("主机已注册，注册信息： %s" % uuid)
        sys.exit(0)
    request = urllib2.Request("http://%s" % api_service + register_url)
    request.add_header('content-type', 'application/json')
    data = {"id": uuid}
    response = urllib2.urlopen(request, urllib.urlencode(data))
    logger.info(response.read())
    if response.getcode() == 201:
        __write_register(uuid)
        print("注册成功 %s" % uuid)
    print("注册成功 %s" % uuid)


def unregister(uuid):
    status = __check_register(uuid)
    if not status:
        print("主机 %s 未注册" % uuid)

    request = urllib2.Request("http://%s" % api_service + register_url + "/%s" % uuid)
    request.get_method = lambda: 'DELETE'
    request.add_header('content-type', 'application/json')
    response = urllib2.urlopen(request)
    logger.info(response.read())
    if response.getcode() == 200:
        __remove_register()


def help():
    print("usage:\n"
          "python register.py <register/unregister> <uuid>\n")


if __name__ == '__main__':
    try:
        action = sys.argv[1]
        uuid = sys.argv[2]
    except IndexError as e:
        print("缺少必要参数\n")
        help()
        sys.exit(1)

    if action == "register":
        register(uuid)
    elif action == "unregister":
        unregister(uuid)
    else:
        print("usage error")
        help()
