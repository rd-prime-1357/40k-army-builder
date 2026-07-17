#!/usr/bin/env python3
"""
pipeline_manifest.py — D123 file-integrity manifest.

Guards every file named in pipeline_manifest.json against a SHA-256 content hash,
so a wrong copy of any pipeline input, script, harness, or output is caught by name
before anything downstream (repro_check.py, rules_assertions.py) runs.

Usage:
    python3 pipeline_manifest.py --write     # regenerate pipeline_manifest.json from the
                                              # current directory's files (run at session close)
    python3 pipeline_manifest.py             # check current files against the manifest

Importable: check(dir_) -> (ok: bool, message: str), used by rules_assertions.py's P3.
"""
import argparse
import hashlib
import json
import os

MANIFEST_NAME = "pipeline_manifest.json"


def _hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check(dir_):
    manifest_path = os.path.join(dir_, MANIFEST_NAME)
    if not os.path.exists(manifest_path):
        return False, f"{MANIFEST_NAME} not found"
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    files = manifest.get("files", {})
    if not files:
        return False, f"{MANIFEST_NAME} has no 'files' entries"

    mismatches = []
    missing = []
    for name, expected_hash in files.items():
        path = os.path.join(dir_, name)
        if not os.path.exists(path):
            missing.append(name)
            continue
        actual_hash = _hash_file(path)
        if actual_hash != expected_hash:
            mismatches.append(name)

    if missing or mismatches:
        parts = []
        if missing:
            parts.append(f"missing: {', '.join(missing)}")
        if mismatches:
            parts.append(f"hash mismatch: {', '.join(mismatches)}")
        return False, "; ".join(parts)

    return True, f"all {len(files)} guarded files match {MANIFEST_NAME}"


def write(dir_):
    manifest_path = os.path.join(dir_, MANIFEST_NAME)
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as f:
            existing = json.load(f)
        names = list(existing.get("files", {}).keys())
    else:
        raise SystemExit(
            f"{MANIFEST_NAME} does not exist yet — cannot infer which files to guard. "
            "Create it once with the initial file list, then use --write to refresh hashes."
        )

    new_files = {}
    missing = []
    for name in names:
        path = os.path.join(dir_, name)
        if not os.path.exists(path):
            missing.append(name)
            continue
        new_files[name] = _hash_file(path)

    if missing:
        print(f"WARNING: {len(missing)} guarded file(s) not found, left out of the "
              f"regenerated manifest: {', '.join(missing)}")

    out = {
        "_note": "SHA-256 of every guarded pipeline file. Regenerated at session close "
                 "(python3 pipeline_manifest.py --write). manifest_check verifies it at "
                 "baseline; a mismatch names the file that arrived as the wrong copy.",
        "files": new_files,
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
        f.write("\n")
    print(f"Wrote {len(new_files)} file hashes to {manifest_path}")


def main():
    parser = argparse.ArgumentParser(description="D123 pipeline file-integrity manifest.")
    parser.add_argument("--dir", default=".", help="Directory containing the guarded files.")
    parser.add_argument("--write", action="store_true",
                         help="Regenerate the manifest's hashes from current files.")
    args = parser.parse_args()

    dir_ = os.path.abspath(args.dir)
    if args.write:
        write(dir_)
        return

    ok, msg = check(dir_)
    print(("OK   " if ok else "FAIL ") + msg)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
