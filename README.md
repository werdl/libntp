## libntp
### NTP for Python
- An alternative to ntplib
- Easy API
- Simple include
### An example
```py
import libntp
myobj=libntp.ntp()
myobj.request()
print(myobj.iso8601)

print(libntp.ntp.local_utc())
```
