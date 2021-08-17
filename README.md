# ning-utils

A collection of convenience scripts.

- [**validate-gs-checksums.py**](https://github.com/ning-y/ning-utils/blob/master/validate-gs-checksums.py) checks of two files (local or on Google Cloud Storage) are the same, based on their CRC32c hash as computed by [gsutil](https://cloud.google.com/storage/docs/gsutil/commands/hash).
- [**tidy-fastq-for-bssh.py**](https://github.com/ning-y/ning-utils/blob/master/tidy-fastq-for-bssh.py) generates a bash command to tidy FASTQ files (of a specific convention, from a specific sequencing company) for BSSH upload.
