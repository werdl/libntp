import socket
import struct
import time
import datetime


class ntp:
    """
    A class for dealing with NTP requests. It also provides methods for 
    formatting dates according to both the MM-DD-YYYY HH:MM:SS and ISO8601 
    formats. It can deal with local timezones and has no external depenencies.

    In the henceforth documentation, MM-DD-YYYY HH:MM:SS will be referred to
    as 'UTC format'.
    """
    def __init__(self):
        """
        Initialize the object with a 0 value for the Unix TS, 
        and the system time for the date object.
        """
        self.unix=0
        self.date_object=datetime.datetime.strptime("12 October, 2023", "%d %B, %Y")
    def utc(self, offset=0):
        """
        Return the date_object property formatted in UTC format.
        `offset` - UTC offset in hours (can be floating-point)
        """
        dt_offset=datetime.datetime.fromtimestamp(self.unix,# init with Unix TS
                                            tz=datetime.timezone(
                                                datetime.timedelta(
                                                    minutes=(
                                                        offset*60
                                                        # multiply offset by 60
                                                        # to get a value in
                                                        # minutes. Specified as
                                                        # a floating point number
                                                        # for full compatability.
                                                    )
                                                )
                                            )
                                        )
        return dt_offset.strftime("%m-%d-%Y %H:%M:%S")
    def iso8601(self, offset=0):
        """
        Return the date_object formatted in ISO8601
        `offset` - UTC offset in hours (can be floating-point)
        """
        dt_offset=datetime.datetime.fromtimestamp(self.unix,
                                                tz=datetime.timezone(
                                                    datetime.timedelta(
                                                        minutes=round(
                                                                offset*60
                                                                # same offsetting
                                                        )
                                                      )
                                                    )
                                                )
        return dt_offset.strftime("P%Y-%m-%dT%H:%M:%S%z")
   
    def request(self, addr='ptbtime1.ptb.de'):
        """
        Sets the class variables to the appropriate values, from the ping.
        `addr` - NTP server to ping, by default set to the German metrology 
        institute.
        """
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
        """
        Internal method that returns the current timezone.
        This information is user set in the environment variables.
        This is mainly for the static easy-use methods.
        """
        if time.daylight:
            return datetime.timezone(
                datetime.timedelta(seconds=-time.altzone),
                                     time.tzname[1])
        else:
            return datetime.timezone(
                datetime.timedelta(seconds=-time.timezone),
                                     time.tzname[0])
    @staticmethod
    def __tzstr():
        """
        Internal method that formats the UTC offset as a string.
        Examples:
            +7
            -8
            +0
        """
        raw_float=datetime.datetime.now(
                tz=ntp.__currenttz()
            ).utcoffset().total_seconds()/60/60
        if abs(raw_float)==raw_float:
            return f"+{raw_float}"
        else:
            return f"-{raw_float}"

    @staticmethod
    def request_utcr(offset_hour = 0):
        """
        Quick access UTC formatted date, offset in hours
        """
        self=ntp()
        self.request()
        return self.utc(offset_hour)
    
    @staticmethod
    def iso8601r(offset_hour = 0):
        """
        Quick access ISO8601 formatted date, offset in hours
        """
        self=ntp()
        self.request()
        return self.iso8601(offset_hour)

    @staticmethod
    def local_utc():
        """
        Quick access UTC formatted date, offset in hours, in local TZ
        """
        self=ntp()
        self.request()
        return self.request_utcr(float(ntp.__tzstr()))

    @staticmethod
    def local_iso8601():
        """
        Quick access ISO8601 formatted date, offset in hours, in local TZ
        """
        self=ntp()
        self.request()
        return self.iso8601r(float(ntp.__tzstr()))
print(ntp.local_iso8601())
