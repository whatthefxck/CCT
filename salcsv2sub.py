import sys
import os
import csv

def convert(inp, channel):
    rows = []
    with open(inp, newline="") as f:
        r = csv.reader(f)
        header = next(r)
        col = channel + 1
        target = "channel %d" % channel
        for i, name in enumerate(header):
            if name.strip().lower() == target:
                col = i
                break
        for row in r:
            if len(row) <= col:
                continue
            try:
                t = float(row[0])
                lvl = int(row[col])
            except ValueError:
                continue
            rows.append((t, lvl))

    timings = []
    for i in range(len(rows) - 1):
        lvl = rows[i][1]
        d = (rows[i + 1][0] - rows[i][0]) * 1e6
        if d <= 0:
            continue
        v = int(round(d))
        if v < 1:
            v = 1
        val = v if lvl == 1 else -v
        if timings and (timings[-1] > 0) == (val > 0):
            timings[-1] += val
        else:
            timings.append(val)

    lines = [
        "Filetype: Flipper SubGhz RAW File",
        "Version: 1",
        "Frequency: 433920000",
        "Preset: FuriHalSubGhzPresetOok650Async",
        "Protocol: RAW",
    ]
    for i in range(0, len(timings), 512):
        lines.append("RAW_Data: " + " ".join(str(v) for v in timings[i:i + 512]))

    out = os.path.splitext(inp)[0] + ".sub"
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    convert(sys.argv[1], int(sys.argv[2]))