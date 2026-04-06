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

<img width="1919" height="1025" alt="image" src="https://github.com/user-attachments/assets/85cfa7c6-fc4e-4078-9f0a-ad543d1f5d84" />

A detailed look at one of the DATA_FRAG packets showed that the data was being transmitted in fragments by the same RTPS writer (0x00001403). The packet structure contained the fragmentStartingNum, fragmentsInSubmessage, fragmentSize, and sampleSize fields, with the total sample size being 36628 bytes. This confirmed that a large serialized object was being transmitted through this stream, which became the main target of further analysis.

<img width="1919" height="1024" alt="image" src="https://github.com/user-attachments/assets/84f3db21-3eb5-4d18-bd88-719b94803c4a" />

Inspecting a regular RTPS DATA packet showed that the payload was stored as serializedData using CDR_LE encapsulation. It also revealed a different writerEntityId than the fragmented stream, indicating that multiple RTPS writers were active and that not all packets carried the same type of data.



0x00001403 - large DATA_FRAG, sampleSize 36628;
0x00001503 - smaller DATA with serializedData;
Conclusion: The main payload most likely carries exactly: 0x00001403

<img width="1919" height="1019" alt="image" src="https://github.com/user-attachments/assets/ae34af7f-871c-4bcf-beb6-7d1f47bbade8" />

After searching not in the packet list, but directly in the raw bytes, I managed to get to the IPv4 fragment of a large message that Wireshark collected in frame #143. I used the query rgb for the search, since it is a characteristic name for the color field in structures such as point clouds and is a much more reliable indicator than short single-letter fields x, y or z. Strings like x, y and z began to appear in the content of this payload, which indicated the presence of structured coordinate fields. Together, this became another argument in favor of the fact that the stream is not transmitting plain text, but a serialized spatial object.


<img width="1919" height="1024" alt="image" src="https://github.com/user-attachments/assets/01c307ba-3242-47d3-bda3-ca13c0dfcd8d" />

After moving to the collected packet #143, it became clear that the RTPS message contained several DATA_FRAG fragments. Inside each fragment was serializedData, and the encapsulation format was defined as CDR_LE, i.e. the payload was a serialized binary object. The presence of HEARTBEAT_FRAG with the same writer (0x00001403) further confirmed that the same RTPS writer was transmitting a large sample, divided into ten parts.

To verify the data, several (2–3) similar RTPS DATA_FRAG packets were additionally analyzed. The purpose of the verification was to confirm that the recorded behavior is a stable series of large samples, and not a single case.

<img width="1919" height="1022" alt="image" src="https://github.com/user-attachments/assets/735e2838-b20c-4774-a39c-7939ff5caa8a" />

To obtain the final message, I, together with the artificial intelligence, wrote a small Python script that collected IPv4 fragments, extracted the RTPS DATA_FRAG message from the main writer (0x00001403) and restored the serialized payload. The conclusion that this payload is point cloud data was not made by chance: during analysis in Wireshark, it became clear that a large fragmented CDR-serialized object was being transmitted, and fields such as x, y and z, characteristic of spatial coordinates, began to appear in its content. In addition, the structure of the restored data corresponded to the typical point cloud format, where each point is described by coordinates and an additional color value. Therefore, the restored payload was interpreted as point cloud data, after which an X-Z projection was constructed for the top layer. It was this visualization that revealed the hidden text.


## FLAG: RS{D4vy_J0nes_Sp3aks_1n_5il3nce}
