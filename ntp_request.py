import socket
import struct
import sys
import time
import datetime
import pytz


class ntp:
    def __init__(self):
        self.unix=0
        self.date_object=datetime.datetime.strptime("12 October, 2023", "%d %B, %Y")
    def utc(self, offset=0):
        dt_offset=datetime.datetime.fromtimestamp(  self.unix,
                                            tz=datetime.timezone(
                                                datetime.timedelta(
                                                    minutes=round(
                                                        offset*60
                                                    )
                                                )
                                            )
                                        )
        return dt_offset.strftime("%m-%d-%Y %H:%M:%S")
    def iso8601(self, offset=0):
        dt_offset=datetime.datetime.fromtimestamp(  self.unix,
                                                    tz=datetime.timezone(
                                                        datetime.timedelta(
                                                            minutes=round(
                                                                offset*60
                                                            )
                                                        )
                                                    )
                                                )
        return dt_offset.strftime("P%Y-%m-%dT%H:%M:%S%z")
   
    def request(self, addr='ptbtime1.ptb.de'):
        REF_TIME_1970 = 2208988800  # Reference time
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = b'\x1b' + 47 * b'\0' # ping
        client.sendto(data, (addr, 123))
        data, _ = client.recvfrom(1024)
        if data:
            t = struct.unpack('!12I', data)[10]
            t -= REF_TIME_1970
        self.unix=t
        self.date_object=datetime.datetime.fromtimestamp(t)
        return time.ctime(t), t
    
    @staticmethod
    def __currenttz():
        if time.daylight:
            return datetime.timezone(datetime.timedelta(seconds=-time.altzone),time.tzname[1])
        else:
            return datetime.timezone(datetime.timedelta(seconds=-time.timezone),time.tzname[0])
    @staticmethod
    def tzint():
        raw_float=datetime.datetime.now(ntp.__currenttz()).utcoffset().total_seconds()/60/60
        if abs(raw_float)==raw_float:
            return f"+{raw_float}"
        else:
            return f"-{raw_float}"

    @staticmethod
    def request_utcr(offset_hour = 0):
        self=ntp()
        self.request()
        return self.utc(offset_hour)
    
    @staticmethod
    def iso8601r(offset_hour = 0):
        self=ntp()
        self.request()
        return self.iso8601(offset_hour)

    @staticmethod
    def local_utc():
        self=ntp()
        self.request()
        return self.request_utcr(float(ntp.tzint()))

    @staticmethod
    def local_iso8601():
        self=ntp()
        self.request()
        return self.iso8601r(float(ntp.tzint()))
print(ntp.local_iso8601())