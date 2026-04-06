<img width="974" height="500" alt="image" src="https://github.com/user-attachments/assets/bdae45dd-3378-4b21-8118-9168c9ddc52e" />

After opening the .pcap file provided by the organizers, I performed an initial analysis of the network dump in Wireshark. It was found that the file contained both service network traffic and the main UDP flow between two IP addresses. Further analysis consisted of isolating this flow, identifying the upper-layer protocol, and searching for data that could contain a hidden message.
