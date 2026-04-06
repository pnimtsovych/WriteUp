<img width="1918" height="1021" alt="image" src="https://github.com/user-attachments/assets/dbcf59af-e0ca-488e-aff6-7979e3175c1e" />


After opening the .pcap file provided by the organizers, I performed an initial analysis of the network dump in Wireshark. It was found that the file contained both service network traffic and the main UDP flow between two IP addresses. Further analysis consisted of isolating this flow, identifying the upper-layer protocol, and searching for data that could contain a hidden message.

<img width="1526" height="829" alt="image" src="https://github.com/user-attachments/assets/ec8fc5ea-6c26-4695-a10e-7335e6d0d880" />

I began by checking the protocol hierarchy in Wireshark to understand the overall structure of the capture. Although the dump contained some ARP, ICMP, and a small amount of IPv6 traffic, the overwhelming majority of bytes belonged to RTPS over UDP and IPv4. This indicated that RTPS was the primary protocol of interest and the most likely place where the hidden data was stored.

<img width="1919" height="771" alt="image" src="https://github.com/user-attachments/assets/f7b34c42-f03b-4f6b-b363-49a5b6bb9769" />

<img width="1919" height="784" alt="image" src="https://github.com/user-attachments/assets/6ea0c4df-0d86-4152-8634-7de0923e4809" />


After reviewing the IPv4 conversation statistics, it became clear that the main data exchange was taking place between 10.42.0.11 and 10.42.0.10. It was also noticed that a significantly larger amount of data was transferred in the direction from 10.42.0.11 to 10.42.0.10, which indicated that the main payload could be transmitted on this channel.

