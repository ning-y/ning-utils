#!/usr/bin/env python

"""Check checksum equality for two files, possibly on Google Cloud Storage.

The shebang assumes that "python" refers to python3. Remote files on Google
Cloud Storage are indicated by the "gs://" prefix. gsutil must be on PATH, and
already configured.
"""

import argparse, re, subprocess, sys

parser = argparse.ArgumentParser(
    prog="validate-gs-checksums",
    description=("Check checksum equality for two files, "
                 "possibly on Google Cloud Storage. "
                 "gsutil must be on PATH and configured. "
                 "If equal, exit code 0; else if hashing error, exit code 2; "
                 "otherwise (checksums not equal) exit code 1."))
parser.add_argument(
    "file", nargs=2,
    help=('File to check. If on Google Cloud Storage, prefix with "gs://"'))
args = parser.parse_args()

# -c is "Calculate a CRC32c hash for the file"
make_gsutil_command = lambda fn: ["gsutil", "hash", "-c", fn]

# commands is a map of lists, completed process a map of
# subprocess.CompletedProcess, stdouts a map of strings, hashes a list of
# re.match or None.
commands = map(make_gsutil_command, args.file)
completed_processes = map(
    lambda args: subprocess.run(args, check=True, capture_output=True),
    commands)
stdouts = map(lambda cproc: cproc.stdout.decode(), completed_processes)
hashes = list(map(
    lambda stdout: re.search("(?<=:)\s+[^\s]+$", stdout), stdouts))

if hashes[0] is None and hashes[1] is None:
    print("Failed to hash both files.", file=sys.stderr)
    sys.exit(2)
elif None in hashes:
    print(f"Failed to hash {arg.file[hashes.index(None)]}", file=sys.stderr)
    sys.exit(2)

hashes = list(map(lambda match: match.group(0).strip(), hashes))
print(f"Respective hashes (crc32c): {hashes[0]}\t{hashes[1]}")

if hashes[0] == hashes[1]: sys.exit(0)
else: sys.exit(1)
