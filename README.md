
# BrawlStars latency tests packets filterer

This project includes a python script made to filter out brawl stars latency test packets, based on [scapy](https://pypi.org/project/scapy/) and [pydivert](https://pypi.org/project/pydivert/)

The ip geolocation local database ( so we dont have to use an api ) is zipped due to the big file size, for usage just un-zip it and place it on the root

# Protocol

BrawlStars use latency testing protocol to determine the best server for the player that is willing to play at the time. We cant manipulate the specific server which it will connect us to but we can manipulate the location.

BrawlStars always sends us 19 battle server IPs in an encrypted TCP connection. After the client recieves these, it playes a ping pong with each of them consisting of 6 pings ( from client ) and 5 pongs ( reply from server ).

After ping-pongs are done it sends back the results to the TCP server in an encrypted message. TCP server then determines the best one and sends client everything he needs to know to establish a secure connection with the selected battle server.

As the TCP server part encryption is complex i decided to rather look at the ping-pong packet structure, with a little knowledge of the structure we can filter them out and only let the ones we want leave our pc ( the rest will be timed-out therefore it will select the only one it got results from )

## Features

- Simple CLI
- Country filtering based on ip geo-location
- Error logging


## Appendix

Please note that BrawlStars has a so called latency-session which long story short means this:

1.When all 19 latency ping-pongs are succesfully recieved it keeps the selected server chached on the TCP server, however if only one ping-pong is timed-out or crashed, the selected server isn't chached

2.This means that if BrawlStars will run latency tests without you filtering the netowrk at the time, it will keep the result chached and you won't be able to change the battle server using the method mentioned earlier

