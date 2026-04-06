<img width="1918" height="1021" alt="image" src="https://github.com/user-attachments/assets/dbcf59af-e0ca-488e-aff6-7979e3175c1e" />


After opening the .pcap file provided by the organizers, I performed an initial analysis of the network dump in Wireshark. It was found that the file contained both service network traffic and the main UDP flow between two IP addresses. Further analysis consisted of isolating this flow, identifying the upper-layer protocol, and searching for data that could contain a hidden message.

<img width="1526" height="829" alt="image" src="https://github.com/user-attachments/assets/ec8fc5ea-6c26-4695-a10e-7335e6d0d880" />

I began by checking the protocol hierarchy in Wireshark to understand the overall structure of the capture. Although the dump contained some ARP, ICMP, and a small amount of IPv6 traffic, the overwhelming majority of bytes belonged to RTPS over UDP and IPv4. This indicated that RTPS was the primary protocol of interest and the most likely place where the hidden data was stored.
