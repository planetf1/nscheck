Simple script to check effective ping times, accounting for DNS nameservers, to sites important to me

The objective was to determine
 - whether my ISP server (IP hardcoded) gives 'closer' results that select public nameservers
 - how cloudflare/quad9/controld etc compare
 - whether EDNS helps with quad9

I am ~80km from London, with good fibre connectivity (900/110) via British Telecom, having recently moved
from an ISP where I was getting issues.

Script limitations
 - Only a single 'dig' is done. This isn't really representative of performance as it will depend on caching
 - times should be limited to 2 digits probably!
 - some traceroutes simply run out of hops due to no resposne
 - sometimes the same IP address gets routed differently -- so not due to the nameserver

   
Example output:

```
Results for google.co.uk:
+------------------+------------------------+-----------------+---------------+--------------------+---------------+-----------------+
|    DNS Server    | DNS Response Time (ms) |   Resolved IP   | Min Ping (ms) |  Median Ping (ms)  | Max Ping (ms) | Traceroute Hops |
+------------------+------------------------+-----------------+---------------+--------------------+---------------+-----------------+
|  dns.quad9.net   |   26.879072189331055   | 142.250.187.195 |      2.96     | 4.140000000000001  |      5.13     |        10       |
| dns11.quad9.net  |   36.200523376464844   | 142.250.187.195 |      2.94     | 3.9450000000000003 |      5.63     |        8        |
| one.one.one.one  |    17.547607421875     | 142.250.179.227 |      3.37     |       4.265        |      5.27     |        9        |
|  dns.google.com  |   57.37733840942383    | 142.250.187.195 |      3.08     |        4.19        |      44.6     |        10       |
|   62.6.40.178    |   17.244338989257812   | 142.250.187.195 |      2.95     |       4.055        |      4.79     |        10       |
| dns.controld.com |   32.10115432739258    |  142.250.178.3  |      2.88     |       4.105        |      4.82     |        9        |
+------------------+------------------------+-----------------+---------------+--------------------+---------------+-----------------+
```
