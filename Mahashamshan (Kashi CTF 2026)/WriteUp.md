<img width="1919" height="1019" alt="image" src="https://github.com/user-attachments/assets/1d13654d-7e0c-4201-9bfb-d80f94324d49" />

During the initial inspection of the pcap in Wireshark, most traffic appeared to be ordinary background noise: TCP SYN/ACK packets, ARP requests, and ICMP. However, several packets stood out as Fragmented IP protocol (proto=TCP 6, off=40, ID=...). Since the challenge explicitly hinted that “the fragment offset field hides more than offset”, these packets immediately became the main focus of the analysis.

<img width="1919" height="1020" alt="image" src="https://github.com/user-attachments/assets/bb9f1395-6c47-4d47-ab7d-035bfafda498" />

A detailed look at one of the suspicious Fragmented IP protocol packets revealed an HTTP-like payload (POST /api/v1/sync HTTP/1.1), but it turned out to be a distraction. This confirmed that the hidden data should be looked for in the header fields, not in the payload.

<img width="1918" height="1025" alt="image" src="https://github.com/user-attachments/assets/1f5a6dcc-b508-4553-8cee-126b4cb6b6fc" />

After analyzing one of the packets marked as Fragmented IP protocol, it was found that its Data field contained an HTTP-like string POST /api/v1/sync HTTP/1.1. Further inspection showed that this same fragment is repeated in all suspicious packets of the same type. Since filtering by fragment offset fields in Wireshark did not provide a stable selection, the filter frame contains "POST /api/v1/sync" was used for practical isolation of this group. This allowed collecting all relevant packets, which were then analyzed at the header field level.
