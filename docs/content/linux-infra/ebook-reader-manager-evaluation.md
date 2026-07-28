---
tags:
  - self-hosting
  - ebooks
---

# Evaluating self-hosted ebook readers & managers

Notes from picking a self-hosted app to run a PDF-heavy ebook/comic library. The
useful learnings, not a product review.

## The one tension that explains every tool

Every tool sits on one side of a fault line — **who owns the files**:

- **Library-owns-the-files** (Calibre, Calibre-Web, and — on import — BookLore/Grimmory):
  metadata can be baked in, but the tool **reorganises files** into `Author/Title/`
  and often **renames** them. Tidy catalogue, mangled layout.
- **Folder-is-the-truth** (Kavita, Komga, Ubooquity): your files/folders are left
  untouched, but metadata lives **inside the app's database** — not portable, and the
  editors tend to be basic.

No product straddles this cleanly, because the two rest on opposite premises. Decide
which you care about more *first*; everything else follows.

## PDF vs EPUB metadata (the part I had wrong)

- **You *can* update PDF metadata** — Title, Author, Subject, Keywords are writable
  in place (`exiftool`, `pdftk`, `qpdf`, Calibre's `ebook-meta`). Not exotic.
- **But PDF has no standard slot for *rich* book metadata** (series, ISBN, tags,
  ratings, multi-author, description). **EPUB does** (the OPF inside the file). So rich
  metadata for PDFs has nowhere portable to live *inside* the file.
- ⇒ For PDFs, the right home for rich metadata is a **sidecar file next to the book**,
  not inside it. That's not a workaround — it's the correct mechanism.

## Sidecars — the actual resolution

A **sidecar** is a metadata file stored *beside* the book (`Book.metadata.json` or the
standard `Book.opf`, often with `Book.cover.jpg`). It gives you the combination that
"doesn't exist as a single product":

- edit metadata **once**, kept **portable**, **originals preserved** (byte-for-byte if
  you don't also embed), and **no folder reorg**.

Formats:

- **`.opf`** (Calibre) — the *standard*; other tools read it. Calibre writes it, but
  only via the desktop/`calibredb`/CWA layer — **plain Calibre-Web keeps edits in
  `metadata.db` only** (DB-locked). Non-destructive to PDFs by default.
- **`.metadata.json`** (BookLore/Grimmory) — portable as data, but a **non-standard**
  dialect; convertible to OPF only with a small script.
- **Kavita: no sidecar at all** — it only *reads* metadata embedded in files
  (`ComicInfo.xml` in CBZ, OPF in EPUB), never PDFs, and never exports. DB-locked.

## Comparison (against: files-in-place · edit metadata · portable sidecar · dedup)

| Tool | Files in place | Edit metadata | Portable sidecar | Dedup |
| --- | --- | --- | --- | --- |
| **Kavita** | ✅ | ⚠️ basic | ❌ (DB only) | ❌ |
| **Komga** | ✅ (per-folder series) | ⚠️ | ❌ | ❌ |
| **Ubooquity** | ✅ (mirrors folder tree) | ❌ | ❌ | ❌ |
| **Calibre-Web / CWA** | ❌ (`Author/Title/`) | ✅✅ | ✅ **`.opf` (standard)** via calibredb | ⚠️ title+author |
| **BookLore / Grimmory** | ✅ *scan* · ❌ *upload reorganises* | ✅✅ | ✅ `.metadata.json` | ❌ |

**No tool does content-signature dedup** (reject the same book by hash/pages/size).
Even Calibre only warns on title+author. If you truly need it, it's a script on top of
whichever tool's REST API.

## Readers & cross-device progress sync

The reading experience is separate from the manager. Connect readers via:

- **OPDS** — the universal catalogue feed. *It is not a web page* — pasting the OPDS
  URL into a browser just hands the Atom feed to your feed reader (Thunderbird). Paste
  it **into a reader app**. Auth is HTTP Basic.
- **Komga-compatible API** — some managers (incl. Grimmory) *speak Komga's protocol*,
  so **Komga clients** (Panels on Mac/iOS, **Mihon** + Komga extension on Android,
  Komelia) connect and **write reading progress back to the server** → Mac ↔ iPhone ↔
  Android agree on your position. This is the clean way to get unified progress sync.
- **KOReader** (+ a sync plugin) for e-ink / Kindle / Kobo.

Gotchas:

- Desktop OPDS readers (e.g. **Thorium**) **download/repackage a local copy** to read
  offline — on macOS under `~/Library/Application Support/EDRLab.ThoriumReader/`
  (as a `.webpub`, not a recognisable PDF). App-private, *not* in your scanned/backed-up
  folders — but be aware it's a copy.
- **Panels** on the App Store is easily confused with a **wallpapers** app of the same
  name — the reader is *"Panels – Comic Reader"* by Produkt. It's PDF/comic-focused
  (weak EPUB).
- For a truly **zero-copy** read, use the manager's **built-in web reader** in a browser.

## Other gotchas worth remembering

- **Filebrowser** (nice web upload/file-drop): the original `filebrowser/filebrowser`
  is **archived/EOL (2026-09-01)** — use the maintained fork **`gtstef/filebrowser`
  (Quantum)**, which also adds a real REST API.
- **BookLore was abandoned in early 2026**; the maintained successor is **Grimmory**
  (`grimmory-tools/grimmory`) — a drop-in fork that still says `booklore` internally.
- Grimmory's **`DISK_TYPE`**: `NETWORK` disables destructive file ops (move/rename)…
  **but also disables sidecar writes** — protecting files and writing sidecars are the
  same "write to the library" capability, so you can't have both. Use `LOCAL` and turn
  **Auto-Move OFF** to keep files put while still writing sidecars.
- Bulk **auto-fetch metadata** (Google Books) rate-limits and mis-matches badly on
  large batches — import with auto-fetch **off**, enrich per-book later.

## Where I landed

**Grimmory** — because it uniquely gives *files-in-place (scan mode) + rich editing +
portable sidecars + a real reader story* (built-in reader, OPDS, Komga-API progress
sync) + a scriptable REST API. Accept its one real gap (no dedup) and the managed-folder
behaviour on *upload*. Kavita stays parked for possible special-case libraries;
Calibre-Web remains the fallback if the **standard OPF** sidecar ever matters more than
Grimmory's JSON.
