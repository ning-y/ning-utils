# ning-utils

A collection of convenience scripts.

- [**pdfaddpw.py**](pdfaddpw.py) password protects PDF files in-place.
- [**tidy-fastq-for-bssh.py**](tidy-fastq-for-bssh.py) generates a bash command to tidy FASTQ files (of a specific header convention, from a specific sequencing company) for BSSH upload.
- [**validate-gs-checksums.py**](validate-gs-checksums.py) checks of two files are the same, based on their CRC32c hash as computed by [gsutil](https://cloud.google.com/storage/docs/gsutil/commands/hash).
  The files can be local or remote on Google Cloud Storage.
computed by [gsutil](https://cloud.google.com/storage/docs/gsutil/commands/hash).
