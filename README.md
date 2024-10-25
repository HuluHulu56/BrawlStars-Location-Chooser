
# BrawlStars latency tests packets filterer

This project includes a python script made to filter out brawl stars latency test packets, based on [scapy](https://pypi.org/project/scapy/) and [pydivert](https://pypi.org/project/pydivert/)

# Protocol

BrawlStars use latency testing protocol to determine the best server for the player that is willing to play at the time. We cant manipulate the specific server which it will connect us to but we can manipulate the location.

BrawlStars always sends us 19 battle server IPs in an encrypted TCP connection. After the client recieves these, it playes a ping pong with each of them consisting of 6 pings ( from client ) and 5 pongs ( reply from server ).

After ping-pongs are done it sends back the results to the TCP server in an encrypted message. TCP server then determines the best one and sends client everything he needs to know to establish a secure connection with the selected battle server.

As the TCP server part encryption is complex i decided to rather look at the ping-pong packet structure, with a little knowledge of the structure we can filter them out and only let the ones we want leave our pc ( the rest will be timed-out therefore it will select the only one it got results from )
