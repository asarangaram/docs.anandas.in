---
title: Renewing an expiring GPG key
---

# Renewing an expiring GPG key

## An expired key still decrypts

This is the first thing to know, because it decides how urgent the job is.

Expiry is a policy flag in the key's self-signature, not a destruction of the
private key. GnuPG will happily **decrypt** data encrypted to an expired key,
so nothing already encrypted becomes unreadable.

What stops working:

* encrypting *to* that key — `gpg --encrypt --recipient <expired>` refuses
* `pass insert`, if the store is encrypted to it
* new signatures are not trusted

So expiry is an inconvenience. **Losing** the private key is the unrecoverable
event, and the two are often confused.

## Check what actually expires

The primary key and each subkey carry their own expiry. Encryption uses the
subkey marked `[E]`, so that is the one that matters for encrypted data:

```bash
gpg --list-keys --keyid-format=long --with-subkey-fingerprint
```

```
pub   ed25519/AAAA1111BBBB2222 2024-01-01 [SC] [expires: 2027-01-01]
sub   cv25519/CCCC3333DDDD4444 2024-01-01 [E]  [expires: 2027-01-01]
```

Note the two separate `[expires:]` lines: the primary key `[SC]` and the
encryption subkey `[E]` are extended independently.

Machine-readable, for a monitoring script — field 7 is the expiry as a Unix
timestamp, empty when the key never expires:

```bash
gpg --list-keys --with-colons <KEYID> \
  | awk -F: '$1=="sub" && $12 ~ /e/ {print ($7==""?"never":strftime("%Y-%m-%d",$7))}'
```

## Extend it

Renewing means setting a new expiry date on the existing key. You keep the
same key, the same fingerprint, and everything already encrypted to it. You
need the private key and its passphrase, so this must be run interactively.

Non-interactive form (GnuPG 2.1+), extending the primary key and **all**
subkeys by two years:

```bash
gpg --quick-set-expire <FINGERPRINT> 2y
gpg --quick-set-expire <FINGERPRINT> 2y '*'
```

The second line is the one people forget. The first extends only the primary
key, which leaves the `[E]` subkey expired — the half that actually encrypts.
The symptom is confusing, because `--list-keys` shows a valid primary while
encryption still fails.

The interactive equivalent:

```
gpg --edit-key <KEYID>
> expire          # new period for the primary key
> key 1           # select the first subkey
> expire          # extend it too
> save
```

Accepted periods: `0` never, `2y`, `18m`, `90d`, or `YYYY-MM-DD`.

## Redistribute the public key

The new expiry lives in an updated self-signature, so anything holding the old
public key still believes it expires on the old date. Re-export and re-import
everywhere it is used:

```bash
# on the machine holding the private key
gpg --export --armor <KEYID> > key.asc

# on every machine that encrypts to it
gpg --import key.asc
```

If the key is on a keyserver, `gpg --send-keys <KEYID>` as well.

## Back up the private key, separately

Extension does nothing for the real risk. If the private key is lost,
everything encrypted to it is gone — password stores, encrypted archives, the
lot.

```bash
gpg --export-secret-keys --armor <KEYID> > private-key.asc
gpg --export-ownertrust > ownertrust.txt
```

Keep those **off** the machines they protect and off the drive holding the
encrypted data — a USB in a drawer, or printed with
[paperkey](https://www.jabberwocky.com/software/paperkey/). An exported secret
key is as sensitive as it gets; anyone holding it holds everything.

A revocation certificate is worth generating at the same time, while you still
can:

```bash
gpg --output revoke.asc --gen-revoke <KEYID>
```

## Don't get caught out

* Extend the **subkeys**, not just the primary key
* An expired key still decrypts — do not panic-migrate data
* Re-import the public key on other machines, or they keep the old expiry
* Encrypting to two keys, one of which never expires, gives a fallback
* Set a calendar reminder a month ahead; there is no warning otherwise
