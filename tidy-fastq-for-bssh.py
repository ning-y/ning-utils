#!/usr/bin/env python

import argparse, gzip, os.path, re

parser = argparse.ArgumentParser(
    prog="tidy-fastq-for-bssh",
    description=(
        "Tidy FASTQ files of the same sample "
        "for upload to Illumina BaseSpace Sequence Hub."))
parser.add_argument("--output-dir", "-o")
parser.add_argument(
    "--fix-sample-names", action="store_true",
    help=(
        "Modify sample names in FASTQ headers to fit BS requirements. Without "
        "this option, you will have to rely on the --allow-invalid-readnames "
        "option of bs upload dataset."))
parser.add_argument("name", help="Sample name for this sample")
parser.add_argument("fastqs", nargs="+", help="FASTQ files for this sample")
args = parser.parse_args()

def get_first_line_of_gzip(gzipped_file):
    with gzip.open(gzipped_file, "rt") as f:
        return f.readline().strip()

def parse_fastq_read_name(read_name):
    """
    Returns a dictionary of string keys and values.
    Assumes Illumina. See https://web.archive.org/web/20210816033841/https://help.basespace.illumina.com/articles/descriptive/fastq-files/
    E.g. @A00609:40:HWHWMDSXX:1:1101:4363:1000 2:N:0:TGGCTTCA+CCGTGAGA
    """
    space_delimited = read_name[1:].split(" ")
    colon_delimited = [
        *space_delimited[0].split(":"), *space_delimited[1].split(":")]
    field_names = [
        "instrument", "run", "flowcell", "lane", "tile", "x", "y", "read",
        "is_filtered", "control number", "sample number"]
    return dict(zip(field_names, colon_delimited))

# Check that each file is unique
assert len(args.fastqs) == len(set(args.fastqs))

fqs = []
for fn in args.fastqs:
    fq = {"filename": fn, **parse_fastq_read_name(get_first_line_of_gzip(fn))}
    fqs.append(fq)

# Make a map for flowcell IDs
flowcells = list(set([fq["flowcell"] for fq in fqs]))

# Generate shell commands. For the output filenames, see
# https://web.archive.org/web/20210807153645/https://support.illumina.com/help/BaseSpace_Sequence_Hub/Source/Informatics/BS/UploadFastqReq_swBS.htm
for fq in fqs:
    fq["lane"] = int(fq["lane"])
    fq["flowcell"] = flowcells.index(fq["flowcell"]) + 1
    new_filename = f"{args.name}_S1_L{fq['lane']:03d}_R{fq['read']}_{fq['flowcell']:03d}.fastq.gz"

    if args.output_dir:
        new_filename = os.path.join(args.output_dir, new_filename)

    should_sanitise_sample_number = re.match("^\d+$", fq["sample number"]) is None

    if not (should_sanitise_sample_number and args.fix_sample_names):
        print(f"cp {fq['filename']} {new_filename}")
    else:
        # For multi-lane samples, a FASTQ file can sometimes have different
        # sample numbers, so we cannot rely on sed using fq['sample_number'].
        print((
            f"zcat {fq['filename']} | "
            """awk '{if (NR % 4 == 1) {gsub(/:[^:]+$/,":1"); print} else {print}}' | """
            f"gzip > {new_filename}"))
