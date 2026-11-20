#!/usr/bin/env python3
"""Entry for make.fun news-image-20261120:
"Sum up 20 November's world news in one image".

The poster is rendered ahead of time and shipped in this repository
as entry.png. This program only copies it, byte for byte, to the
output directory, so both runs of the entry write exactly the same
bytes. Standard library only; no network, no clock, no randomness.

The copy is written to a temporary file in the output directory and
only moved into place (os.replace) once its hash is verified, so a
failed or interrupted copy can never leave a partial entry.png behind
and a stale file from an earlier run is never mistaken for this run's
output.

Run it with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
The image lands at out/entry.png.
"""

import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    # Fail loudly instead of writing a broken entry: the shipped image
    # must exist and must not be empty.
    try:
        source_size = os.path.getsize(SOURCE)
    except OSError as exc:
        raise SystemExit("entry.png missing next to main.py: %s" % exc)
    if source_size == 0:
        raise SystemExit("entry.png is empty, refusing to write an empty entry")
    source_hash = sha256_of(SOURCE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)

    target = os.path.join(out_dir, "entry.png")
    tmp_fd, tmp_path = tempfile.mkstemp(prefix=".entry-", dir=out_dir)
    try:
        with os.fdopen(tmp_fd, "wb") as tmp_fh:
            with open(SOURCE, "rb") as src_fh:
                shutil.copyfileobj(src_fh, tmp_fh, 65536)
        # The copy must be exact: same bytes in, same bytes out.
        # Compare the hash, not just the size, so a truncated copy
        # cannot pass — and check before the file becomes entry.png.
        if sha256_of(tmp_path) != source_hash:
            raise SystemExit(
                "entry.png copy mismatch: hash differs from source")
        os.replace(tmp_path, target)
    except BaseException:
        # Never leave a half-written temp file behind.
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    print("wrote %s (%d bytes, sha256 %s)" % (target, source_size, source_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
