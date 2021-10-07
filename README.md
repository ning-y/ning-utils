# ning-utils

A collection of convenience scripts.

- [**pdfaddpw.py**](pdfaddpw.py) password protects PDF files in-place.
- [**validate-gs-checksums.py**](validate-gs-checksums.py) checks of two files are the same, based on their CRC32c hash as computed by [gsutil](https://cloud.google.com/storage/docs/gsutil/commands/hash).
  The files can be local or remote on Google Cloud Storage.
