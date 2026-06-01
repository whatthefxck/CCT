# Capture Conversion Tools

> **Experimental — use at your own risk.**

---

## salcsv2sub.py

Convert Saleae Logic Analyzer 1.x/2.x exported `.csv` files to Flipper `.sub` format.

```
python salcsv2sub.py digital.csv [channel 0-7]
```

---

## sub2sr.py

Convert Flipper `.sub` to `.sr` (sigrok / PulseView) format.

```
python sub2sr.py RAW_signal.sub
```