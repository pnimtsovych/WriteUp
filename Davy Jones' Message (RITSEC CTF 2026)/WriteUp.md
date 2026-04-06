<img width="1918" height="1021" alt="image" src="https://github.com/user-attachments/assets/dbcf59af-e0ca-488e-aff6-7979e3175c1e" />


After opening the .pcap file provided by the organizers, I performed an initial analysis of the network dump in Wireshark. It was found that the file contained both service network traffic and the main UDP flow between two IP addresses. Further analysis consisted of isolating this flow, identifying the upper-layer protocol, and searching for data that could contain a hidden message.

<img width="1526" height="829" alt="image" src="https://github.com/user-attachments/assets/ec8fc5ea-6c26-4695-a10e-7335e6d0d880" />

I began by checking the protocol hierarchy in Wireshark to understand the overall structure of the capture. Although the dump contained some ARP, ICMP, and a small amount of IPv6 traffic, the overwhelming majority of bytes belonged to RTPS over UDP and IPv4. This indicated that RTPS was the primary protocol of interest and the most likely place where the hidden data was stored.

<img width="1919" height="771" alt="image" src="https://github.com/user-attachments/assets/f7b34c42-f03b-4f6b-b363-49a5b6bb9769" />

<img width="1919" height="784" alt="image" src="https://github.com/user-attachments/assets/6ea0c4df-0d86-4152-8634-7de0923e4809" />


Analysis of the dialogs showed that the main exchange in the dump occurs between 10.42.0.11 and 10.42.0.10, and UDP statistics specified that this traffic is concentrated around port 17911. After that, I filtered the relevant stream and proceeded to analyze its content to determine the protocol used and find potentially hidden data.

<img width="1919" height="1022" alt="image" src="https://github.com/user-attachments/assets/7fad3b2d-8ee4-4771-998e-13b62a137a80" />

<img width="1919" height="1023" alt="image" src="https://github.com/user-attachments/assets/ed039dc1-ec06-4260-b31b-5bbc6d3facc8" />

Since the RTPS stream contained fragmented data submessages, I concluded that the hidden content was likely embedded inside a larger serialized object rather than in ordinary plaintext packets. Therefore, the next step was to inspect the fragmented payload more closely and determine what type of data was being transmitted.
