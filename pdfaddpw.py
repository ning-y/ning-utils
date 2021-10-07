#!/usr/bin/env python3

import argparse, getpass, subprocess

parser = argparse.ArgumentParser(
    prog="pdfaddpw", description="Password protects PDFs in-place")
parser.add_argument("pdfs", nargs="+")
args = parser.parse_args()

password = getpass.getpass()

for pdf in args.pdfs:
    # Without -dNOPAUSE, user must hit <RET> each page.
    # Without -DBATCH, gs remains in REPL mode after job done
    ps_gs = subprocess.Popen([
            "gs", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
            "-dQUIET", "-sOutputFile=-",
            f"-sOwnerPassword={password}", f"-sUserPassword={password}", pdf],
        stdout=subprocess.PIPE)
    ps_sponge = subprocess.Popen(["sponge", pdf], stdin=ps_gs.stdout)
    ps_sponge.wait()
