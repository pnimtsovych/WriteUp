<img width="1919" height="1019" alt="image" src="https://github.com/user-attachments/assets/1d13654d-7e0c-4201-9bfb-d80f94324d49" />

During the initial inspection of the pcap in Wireshark, most traffic appeared to be ordinary background noise: TCP SYN/ACK packets, ARP requests, and ICMP. However, several packets stood out as Fragmented IP protocol (proto=TCP 6, off=40, ID=...). Since the challenge explicitly hinted that “the fragment offset field hides more than offset”, these packets immediately became the main focus of the analysis.

<img width="1919" height="1020" alt="image" src="https://github.com/user-attachments/assets/bb9f1395-6c47-4d47-ab7d-035bfafda498" />

A detailed look at one of the suspicious Fragmented IP protocol packets revealed an HTTP-like payload (POST /api/v1/sync HTTP/1.1), but it turned out to be a distraction. This confirmed that the hidden data should be looked for in the header fields, not in the payload.

<img width="1918" height="1025" alt="image" src="https://github.com/user-attachments/assets/1f5a6dcc-b508-4553-8cee-126b4cb6b6fc" />

After analyzing one of the packets marked as Fragmented IP protocol, it was found that its Data field contained an HTTP-like string POST /api/v1/sync HTTP/1.1. Further inspection showed that this same fragment is repeated in all suspicious packets of the same type. Since filtering by fragment offset fields in Wireshark did not provide a stable selection, the filter frame contains "POST /api/v1/sync" was used for practical isolation of this group. This allowed collecting all relevant packets, which were then analyzed at the header field level.

After isolating 41 matching packets, I compared them. The HTTP-like payload (POST /api/v1/sync HTTP/1.1) was the same in each of them, so it could not directly contain unique flag characters and most likely acted as a decoy. Instead, the IP Identification values ​​and the first bytes of the fragment payload before the POST line changed, which indicated a real covert channel.

Further analysis showed that the bytes payload[4:8] formed a sequence of values ​​of the form 123456 * n, so they could be used as a character ordering key. At the same time, the low-order byte of the IP Identification field, after XORing with 0x21, produced a readable ASCII character. Thus, each of the 41 packets contained exactly one flag character, and its position was determined separately:

order = int.from_bytes(payload[4:8], "big") // 123456

char = chr((ip_id & 0xff) ^ 0x21)

To automate this process, I used a Python script called solve.py. The script went through all the packets in pcap, selected only those that contained the POST /api/v1/sync marker, extracted the order value from payload[4:8], took the low-order byte of the IP Identification, decoded the character via XOR with 0x21, then sorted all the characters by order and combined them into a final string.

PS C:\Users\User\Music\Mahashamshan> py solve.py
(0, 'k', '0x624a', '271001bb00000000')
(1, 'a', '0x6140', '273501bb0001e240')
(2, 's', '0x6052', '275a01bb0003c480')
(3, 'h', '0x5f49', '277f01bb0005a6c0')
(4, 'i', '0x5e48', '27a401bb00078900')
(5, 'C', '0x5d62', '27c901bb00096b40')
(6, 'T', '0x5c75', '27ee01bb000b4d80')
(7, 'F', '0x5b67', '281301bb000d2fc0')
(8, '{', '0x5a5a', '283801bb000f1200')
(9, 'f', '0x5947', '285d01bb0010f440')
(10, 'r', '0x5853', '288201bb0012d680')
(11, '4', '0x5715', '28a701bb0014b8c0')
(12, 'g', '0x5646', '28cc01bb00169b00')
(13, '_', '0x557e', '28f101bb00187d40')
(14, 'b', '0x5443', '291601bb001a5f80')
(15, '1', '0x5310', '293b01bb001c41c0')
(16, 't', '0x5255', '296001bb001e2400')
(17, '5', '0x5114', '298501bb00200640')
(18, '_', '0x507e', '29aa01bb0021e880')
(19, '4', '0x4f15', '29cf01bb0023cac0')
(20, 'r', '0x4e53', '29f401bb0025ad00')
(21, '3', '0x4d12', '2a1901bb00278f40')
(22, '_', '0x4c7e', '2a3e01bb00297180')
(23, 'm', '0x4b4c', '2a6301bb002b53c0')
(24, 'y', '0x4a58', '2a8801bb002d3600')
(25, '_', '0x497e', '2aad01bb002f1840')
(26, '5', '0x4814', '2ad201bb0030fa80')
(27, 'e', '0x4744', '2af701bb0032dcc0')
(28, 'c', '0x4642', '2b1c01bb0034bf00')
(29, 'r', '0x4553', '2b4101bb0036a140')
(30, '3', '0x4412', '2b6601bb00388380')
(31, 't', '0x4355', '2b8b01bb003a65c0')
(32, '_', '0x427e', '2bb001bb003c4800')
(33, 'c', '0x4142', '2bd501bb003e2a40')
(34, '4', '0x4015', '2bfa01bb00400c80')
(35, 'r', '0x3f53', '2c1f01bb0041eec0')
(36, 'r', '0x3e53', '2c4401bb0043d100')
(37, '1', '0x3d10', '2c6901bb0045b340')
(38, '3', '0x3c12', '2c8e01bb00479580')
(39, 'r', '0x3b53', '2cb301bb004977c0')
(40, '}', '0x3a5c', '2cd801bb004b5a00')

FLAG: kashiCTF{fr4g_b1t5_4r3_my_5ecr3t_c4rr13r}
PS C:\Users\User\Music\Mahashamshan>


## FLAG: kashiCTF{fr4g_b1t5_4r3_my_5ecr3t_c4rr13r}
