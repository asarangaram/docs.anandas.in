---
title: Embedding text in a PNG
---

# Embedding text in a PNG

A PNG can carry arbitrary text alongside the image, in *ancillary* chunks that
image viewers ignore but that travel with the file. Useful for stashing
metadata — a caption, a source URL, or (what sent me down this path) an OCR
document embedded next to the image it describes, so a result is a single file
that still opens as an ordinary picture.

There are **three** text chunk types, and picking the wrong one silently
corrupts non-English text.

| Chunk  | Encoding | Compressed | Use it for |
| ------ | -------- | ---------- | ---------- |
| `tEXt` | Latin-1 (ISO-8859-1) | no  | short ASCII/Latin-1 only |
| `zTXt` | Latin-1 | yes (zlib) | long ASCII/Latin-1 |
| `iTXt` | **UTF-8** | optional (zlib) | anything with non-Latin-1 text |

!!! warning "The gotcha"
    `tEXt` and `zTXt` are **Latin-1**. Store Tamil, Hindi, CJK, or an emoji in
    them and it comes back as mojibake. For any text beyond plain ASCII/Latin-1,
    you must use **`iTXt`** — it is the only one that is UTF-8. (My hOCR is
    multilingual, so `iTXt` was the only correct choice.)

## Why you often can't just use a library

Many image libraries only surface `tEXt`. Dart's `image` package, for example,
exposes an `Image.textData` string map — but it writes those entries as `tEXt`
(Latin-1) and reads only `tEXt`. There is no `iTXt` support. So for UTF-8 you
write the chunk bytes yourself and splice it into the encoded PNG, just before
the `IEND` chunk.

## PNG chunk layout

Every chunk is:

```
length (4 bytes, big-endian)  |  type (4 ASCII)  |  data  |  CRC-32 (4 bytes)
```

The CRC-32 is computed over **type + data** (not the length). A PNG is the
8-byte signature `89 50 4E 47 0D 0A 1A 0A` followed by chunks; `IHDR` first,
`IEND` last.

### iTXt data layout

```
keyword          (1–79 bytes, Latin-1)  \0
compression flag (1 byte: 0 = none, 1 = zlib)
compression method (1 byte: 0)
language tag     (Latin-1)              \0   (may be empty)
translated keyword (UTF-8)              \0   (may be empty)
text             (UTF-8, zlib-compressed if the flag is 1)
```

So a compressed `iTXt` with keyword `hOCR` and empty language/translation is:
`"hOCR", 0x00, 0x01, 0x00, 0x00, 0x00, <zlib(utf8(text))>`.

## Writing it (sketch)

```dart
// 1. encode the image normally
final basePng = encodePng(image);

// 2. build the iTXt body + wrap as a chunk (length | type | body | crc32)
List<int> chunk(String type, List<int> data) {
  final body = [...ascii.encode(type), ...data];
  return [...u32(data.length), ...body, ...u32(getCrc32(body))];
}

// 3. splice the new chunk in just before IEND, and you're done
```

Reading it back is the reverse: walk the chunks, find the `iTXt` whose keyword
matches, skip past `keyword \0 flag method langtag \0 transkw \0`, zlib-inflate
the remainder if the flag is 1, then `utf8.decode`.

!!! note "Caveat"
    Ancillary chunks (both `iTXt` and the XMP metadata some tools use) are
    frequently **stripped when an image editor re-saves** the file. Fine if the
    file only ever moves through your own app; if it might be edited elsewhere,
    a container format (e.g. a zip holding image + sidecar) is the only thing
    that can't be silently gutted.
