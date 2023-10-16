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

    Also, P%Y-%m-%dT%H:%M:%S%z will be known as ISO8601.
    I am aware there are different variants, this is this project's one.
    """
    def __init__(self, server: str = 'ptbtime1.ptb.de') -> None:
        """
        Initialize the object with a 0 value for the Unix TS, 
        and the system time for the date object.

        `server`: int - NTP server, by default German metrology institute
        """
        self.unix=0 # unix ts
        self.date_object=datetime.datetime.fromtimestamp(0) # Unix epoch
        self.server=server # ntp server to ping
    def utc(self, offset: float = 0) -> str:
        """
        Return the date_object property formatted in UTC format.

        `offset`: float - UTC offset in hours (can be floating-point)
        """
        dt_offset=datetime.datetime.fromtimestamp(self.unix,# init with Unix TS
                                            tz=datetime.timezone(
                                                datetime.timedelta(
                                                    minutes=(
                                                        offset*60
                                                    )
                                                )
                                            )
                                        )
        return dt_offset.strftime("%m-%d-%Y %H:%M:%S")
    def iso8601(self, offset: float = 0) -> str:
        """
        Return the date_object formatted in ISO8601

        `offset`: float - UTC offset in hours (can be floating-point)
        """
        dt_offset=datetime.datetime.fromtimestamp(self.unix,
                                                tz=datetime.timezone(
                                                    datetime.timedelta(
                                                        minutes=round(
                                                                offset*60
                                                        )
                                                      )
                                                    )
                                                )
        return dt_offset.strftime("P%Y-%m-%dT%H:%M:%S%z")
    def request(self) -> tuple:
        """
        Sets the class variables to the appropriate values, from the ping.
        From the server specified at object creation.
        """
        REF_TIME_1970 = 2208988800  # Reference time
        client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data=b'\x1b' + 47 * b'\0' # ping
        client.sendto(data, (self.server, 123)) # ntp port - 123
        data, _ = client.recvfrom(1024)
        if data:
            t=struct.unpack('!12I', data)[10]
            t-=REF_TIME_1970
        self.unix=t
        self.date_object=datetime.datetime.fromtimestamp(t)
        return (time.ctime(t), t)
    
    @staticmethod
    def __currenttz() -> datetime.timedelta:
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
    def __tzstr() -> str:
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
    def request_utcr(offset_hour: float = 0) -> str:
        """
        Quick access UTC formatted date
        
        `offset_hour`: float - UTC offset in hours (can be float)
        """
        self=ntp()
        self.request()
        return self.utc(offset_hour)
    
    @staticmethod
    def iso8601r(offset_hour: float = 0) -> str:
        """
        Quick access ISO8601 formatted date, offset in hours
        
        `offset_hour`: float - UTC offset in hours (can be float)
        """
        self=ntp()
        self.request()
        return self.iso8601(offset_hour)

    @staticmethod
    def local_utc() -> str:
        """
        Quick access UTC formatted date, offset in hours, in local TZ
        """
        self=ntp()
        self.request()
        return self.request_utcr(float(ntp.__tzstr()))

    @staticmethod
    def local_iso8601() -> str:
        """
        Quick access ISO8601 formatted date, offset in hours, in local TZ
        """
        self=ntp()
        self.request()
        return self.iso8601r(float(ntp.__tzstr()))
