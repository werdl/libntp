## libntp
### NTP for Python
- An alternative to ntplib
- Easy API
- Simple include
- No external dependencies 
### An example
```py
from libntp import ntp
myobj=ntp()
myobj.request()
print(myobj.iso8601())

print(ntp.local_utc())
```
