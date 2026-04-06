#!/usr/bin/env python3
"""Self-contained solver for Davy Jones' Message.

No scapy required.
Reads the pcap directly, reassembles IPv4 fragments,
extracts RTPS DATA_FRAG for writer 0x00001403,
parses PointCloud2-like CDR_LE payloads, and renders the hidden text.

Usage:
    python3 solve_min.py davy_jones_message.pcap

Dependencies:
    pip install numpy matplotlib
"""

from __future__ import annotations

import collections
import struct
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

WRITER_ID = "00001403"


def read_pcap(path: str):
    packets = []
    with open(path, "rb") as f:
        gh = f.read(24)
        if gh[:4] == b"\xd4\xc3\xb2\xa1":
            endian = "<"
        elif gh[:4] == b"\xa1\xb2\xc3\xd4":
            endian = ">"
        else:
            raise ValueError("Not a pcap file")

        while True:
            ph = f.read(16)
            if not ph:
                break
            _ts_sec, _ts_usec, incl_len, _orig_len = struct.unpack(endian + "IIII", ph)
            data = f.read(incl_len)
            if len(data) < 14:
                continue

            eth_type = struct.unpack("!H", data[12:14])[0]
            if eth_type != 0x0800:  # IPv4 only
                continue

            ip = data[14:]
            if len(ip) < 20:
                continue

            ihl = (ip[0] & 0x0F) * 4
            total_len = struct.unpack("!H", ip[2:4])[0]
            ident = struct.unpack("!H", ip[4:6])[0]
            flags_frag = struct.unpack("!H", ip[6:8])[0]
            proto = ip[9]
            src = ".".join(map(str, ip[12:16]))
            dst = ".".join(map(str, ip[16:20]))

            more_fragments = (flags_frag >> 13) & 1
            frag_offset = (flags_frag & 0x1FFF) * 8
            payload = ip[ihl:total_len]

            packets.append(
                {
                    "src": src,
                    "dst": dst,
                    "proto": proto,
                    "id": ident,
                    "fragoff": frag_offset,
                    "mf": more_fragments,
                    "payload": payload,
                }
            )
    return packets


def reassemble_ip(packets):
    groups = collections.defaultdict(list)
    for pkt in packets:
        groups[(pkt["src"], pkt["dst"], pkt["proto"], pkt["id"])].append(pkt)

    out = []
    for frags in groups.values():
        frags = sorted(frags, key=lambda x: x["fragoff"])

        if len(frags) == 1 and frags[0]["fragoff"] == 0 and frags[0]["mf"] == 0:
            frags[0]["full_payload"] = frags[0]["payload"]
            out.append(frags[0])
            continue

        ends = [f["fragoff"] + len(f["payload"]) for f in frags if f["mf"] == 0]
        if not ends:
            continue

        total = max(ends)
        buf = bytearray(total)
        seen = [False] * total
        for frag in frags:
            start = frag["fragoff"]
            end = start + len(frag["payload"])
            buf[start:end] = frag["payload"]
            for i in range(start, end):
                seen[i] = True

        if not all(seen):
            continue

        base = frags[0].copy()
        base["full_payload"] = bytes(buf)
        out.append(base)

    return out


def rtps_submessages(payload: bytes):
    if not payload.startswith(b"RTPS"):
        return
    i = 20
    while i + 4 <= len(payload):
        kind = payload[i]
        flags = payload[i + 1]
        endian = "<" if (flags & 1) else ">"
        length = struct.unpack(endian + "H", payload[i + 2 : i + 4])[0]
        body = payload[i + 4 : i + 4 + length]
        yield kind, body
        i += 4 + length
        if length == 0:
            break


def collect_samples(ip_packets):
    samples: dict[int, dict[str, object]] = {}

    for pkt in ip_packets:
        if pkt["proto"] != 17:  # UDP
            continue

        udp = pkt["full_payload"]
        if len(udp) < 8:
            continue

        _sport, _dport, ulen, _csum = struct.unpack("!HHHH", udp[:8])
        payload = udp[8:ulen]
        if not payload.startswith(b"RTPS"):
            continue

        for kind, body in rtps_submessages(payload):
            if kind != 0x16:  # DATA_FRAG
                continue
            if len(body) < 32:
                continue

            writer = body[8:12].hex()
            if writer != WRITER_ID:
                continue

            writer_sn = struct.unpack("<q", body[12:20])[0]
            frag_start = struct.unpack("<I", body[20:24])[0]
            frags_in_msg = struct.unpack("<H", body[24:26])[0]
            frag_size = struct.unpack("<H", body[26:28])[0]
            sample_size = struct.unpack("<I", body[28:32])[0]
            frag_blob = body[32:]

            entry = samples.setdefault(
                writer_sn,
                {"sample_size": sample_size, "frag_size": frag_size, "frags": {}},
            )
            frags = entry["frags"]
            assert isinstance(frags, dict)

            for j in range(frags_in_msg):
                frag_num = frag_start + j
                start = j * frag_size
                piece = frag_blob[start : start + frag_size]
                if piece:
                    frags[frag_num] = piece

    complete: list[bytes] = []
    for writer_sn in sorted(samples):
        entry = samples[writer_sn]
        sample_size = int(entry["sample_size"])
        frag_size = int(entry["frag_size"])
        frags = entry["frags"]
        assert isinstance(frags, dict)

        needed = (sample_size + frag_size - 1) // frag_size
        if set(frags.keys()) != set(range(1, needed + 1)):
            continue

        data = b"".join(frags[i] for i in range(1, needed + 1))
        complete.append(data[:sample_size])

    return complete


def parse_pointcloud2(sample: bytes):
    off = 0

    def align(n: int):
        nonlocal off
        off = (off + n - 1) & ~(n - 1)

    def u32() -> int:
        nonlocal off
        align(4)
        val = struct.unpack_from("<I", sample, off)[0]
        off += 4
        return val

    def u8() -> int:
        nonlocal off
        val = sample[off]
        off += 1
        return val

    def boolean() -> bool:
        return bool(u8())

    def string() -> str:
        nonlocal off
        n = u32()
        raw = sample[off : off + n]
        off += n
        align(4)
        return raw[:-1].decode("utf-8", errors="ignore") if n else ""

    encapsulation = u32()
    sec = u32()
    nsec = u32()
    frame_id = string()

    height = u32()
    width = u32()

    nfields = u32()
    fields = []
    for _ in range(nfields):
        name = string()
        offset = u32()
        datatype = u8()
        align(4)
        count = u32()
        fields.append((name, offset, datatype, count))

    is_bigendian = boolean()
    align(4)
    point_step = u32()
    row_step = u32()
    data_len = u32()
    data = sample[off : off + data_len]
    off += data_len
    is_dense = boolean()

    points = np.frombuffer(data, dtype="<f4").reshape(-1, 4)
    meta = {
        "encapsulation": encapsulation,
        "sec": sec,
        "nsec": nsec,
        "frame_id": frame_id,
        "height": height,
        "width": width,
        "fields": fields,
        "is_bigendian": is_bigendian,
        "point_step": point_step,
        "row_step": row_step,
        "is_dense": is_dense,
    }
    return meta, points


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 solve_min.py <pcap>")
        return 1

    pcap_path = sys.argv[1]
    if not Path(pcap_path).exists():
        print(f"File not found: {pcap_path}")
        return 1

    raw_packets = read_pcap(pcap_path)
    ip_packets = reassemble_ip(raw_packets)
    samples = collect_samples(ip_packets)
    if not samples:
        print("No complete samples found.")
        return 1

    first_meta = None
    all_points = []
    for sample in samples:
        meta, pts = parse_pointcloud2(sample)
        if first_meta is None:
            first_meta = meta
        all_points.append(pts)

    assert first_meta is not None
    points = np.vstack(all_points)
    x = points[:, 0]
    z = points[:, 2]

    mask = z > 1.0

    print(f"[+] Reassembled samples: {len(samples)}")
    print("[+] First sample metadata:")
    for k, v in first_meta.items():
        print(f"    {k}: {v}")
    print("[+] Rendering X-Z projection to hidden_message.png")

    plt.figure(figsize=(18, 4), dpi=250)
    plt.scatter(x[mask], z[mask], s=0.2)
    plt.gca().set_aspect("equal")
    plt.xlim(-35, 46)
    plt.ylim(3, 7)
    plt.title("Hidden message in X-Z projection (z > 1.0)")
    plt.savefig("hidden_message.png", bbox_inches="tight")
    plt.show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
