import struct

path = "mahashamshan_2.pcap"
rows = []

with open(path, "rb") as f:
    f.read(24)  # pcap global header

    while True:
        hdr = f.read(16)
        if len(hdr) < 16:
            break

        ts_sec, ts_usec, incl_len, orig_len = struct.unpack("<IIII", hdr)
        pkt = f.read(incl_len)

        if len(pkt) < 34:
            continue
        if struct.unpack("!H", pkt[12:14])[0] != 0x0800:
            continue  # not IPv4

        ip = pkt[14:]
        ihl = (ip[0] & 0x0F) * 4
        total_len = struct.unpack("!H", ip[2:4])[0]
        ip_id = struct.unpack("!H", ip[4:6])[0]
        proto = ip[9]
        payload = ip[ihl:total_len]

        if proto != 6:
            continue
        if b"POST /api/v1/sync" not in payload:
            continue

        order = struct.unpack("!I", payload[4:8])[0] // 123456
        ch = chr((ip_id & 0xff) ^ 0x21)

        rows.append((order, ch, hex(ip_id), payload[:8].hex()))

rows.sort()

for row in rows:
    print(row)

flag = "".join(ch for order, ch, _, _ in rows)
print("\nFLAG:", flag)
