import os
import subprocess


class _AccessInfo(object):
    local_ips = []
    not_local = []
    access_ips = []
    access_report = 1

    @classmethod
    def check_local(cls, ip):
        proc = subprocess.Popen("/sbin/ifconfig | grep inet | grep %s" % ip,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                close_fds=True,
                                preexec_fn=os.setsid
                                )
        stdout_value, stderr_value = proc.communicate()
        returncode = proc.returncode
        if returncode:
            cls.not_local.append(ip)
            return False
        if stderr_value:
            cls.not_local.append(ip)
            return False
        if stdout_value.strip("\n"):
            return True
        else:
            cls.not_local.append(ip)
            return False

    @classmethod
    def write_local_ips(cls):
        if cls.local_ips:
            with open("/usr/local/netmap/.info/local", "a") as f:
                for ip in cls.local_ips:
                    f.write(ip + "\n")

                f.flush()

    @classmethod
    def cache_local_ips(cls):
        if os.path.exists("/usr/local/netmap/.info/local"):
            with open("/usr/local/netmap/.info/local") as f:
                for line in f:
                    if line.strip():
                        ip = line.strip("\n")
                        cls.local_ips.append(ip)

        cls.local_ips = list(set(cls.local_ips))

    @classmethod
    def write_access_ips(cls):
        if cls.access_ips:
            with open("/usr/local/netmap/.info/access", "a") as f:
                for ip in cls.access_ips:
                    f.write(ip + "\n")
                f.flush()

    @classmethod
    def cache_access_ips(cls):
        if os.path.exists("/usr/local/netmap/.info/access"):
            with open("/usr/local/netmap/.info/access") as f:
                for line in f:
                    if line.strip():
                        ip = line.strip("\n")
                        cls.access_ips.append(ip)

        cls.access_ips = list(set(cls.access_ips))

    @classmethod
    def is_flush_local_ips(cls, ip):
        if ip in cls.local_ips:
            return True, False
        if ip in cls.not_local:
            return False, False
        if (ip not in cls.local_ips) and (ip not in cls.not_local):
            if cls.check_local(ip):
                cls.local_ips.append(ip)
                cls.write_local_ips()
                return True, True
            else:
                cls.not_local.append(ip)
                return False, False

        return False, False

    @classmethod
    def is_report_access_ips(cls, ip):
        if len(cls.access_ips) > 999:
            cls.access_report = 0
            return False
        if ip not in cls.access_ips:
            cls.access_ips.append(ip)
            cls.write_access_ips()
            return True
        return False


AccessInfo = _AccessInfo
AccessInfo.cache_local_ips()
AccessInfo.cache_access_ips()
