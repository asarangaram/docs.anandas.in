---
title: Japanese filenames
---

# Japanese filenames

Japanese (and other non-ASCII) characters in filenames are indeed treated differently on **Apple’s native file systems** (like **APFS** and older **HFS+**) compared to **exFAT**.

Apple's **APFS** stores filenames in **Unicode NFD** (Normalization Form Decomposed).
- For example, the Japanese character **ガ** ("ga") can be stored as **カ + ゛** (katakana "ka" + combining dakuten mark) instead of the single precomposed code point.
**exFAT** stores filenames in **UTF-16** exactly as given (precomposed stays precomposed, decomposed stays decomposed)

So,
On exFAT, it’s theoretically possible to have two files that _look_ the same (“visually identical”) in Finder but have different Unicode code-points.

Running `rsync` between Mac and exFAT drives, might not match unless **normalized**

Find appropriate solutions when you transfer across different file systems

