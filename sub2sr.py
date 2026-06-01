import sys
import os
import struct
import zipfile

RATE = 1000000

def load_sub(path):
    timings = []
    with open(path) as f:
        for line in f:
            if line.startswith("RAW_Data:"):
                for tok in line[9:].split():
                    timings.append(int(tok))
    return timings

def to_samples(timings):
    out = bytearray()
    for v in timings:
        n = max(1, round(abs(v) * RATE / 1000000))
        out.extend(b"\x01" * n if v > 0 else b"\x00" * n)
    return bytes(out)

def write_sr(out, samples):
    meta = (
        "[global]\n"
        "sigrok version=0.5.2\n"
        "[device 1]\n"
        "capturefile=logic-1\n"
        "total probes=1\n"
        "samplerate=%d Hz\n"
        "total analog=0\n"
        "probe1=D0\n"
        "unitsize=1\n" % RATE
    )
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("version", "2")
        z.writestr("metadata", meta)
        z.writestr("logic-1-1", samples)

def convert(inp):
    timings = load_sub(inp)
    samples = to_samples(timings)
    out = os.path.splitext(inp)[0] + ".sr"
    write_sr(out, samples)

if __name__ == "__main__":
    convert(sys.argv[1])
