#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

from scripts.Config import Config
from scripts.SongFile import SongFile

BUILD_DIR = "build"

def prepare_build_directory():
    try:
        shutil.rmtree(BUILD_DIR)
        os.mkdir(BUILD_DIR)
    except FileExistsError:
        pass

    try:
        os.mkdir(os.path.join(BUILD_DIR, "source"))
    except FileExistsError:
        pass

def transform(path, destdir, config):
    filename = os.path.basename(path)
    destfile = os.path.join(destdir, filename)

    with open(path, "r") as fin:
        with open(destfile, "w") as fout:
            line = fin.readline()
            fout.write(line)

            if config.capo:
                fout.write("\\capo{" + str(config.capo) + "}\n")

            if config.transpose:
                fout.write("\\transpose{" + str(config.transpose) + "}\n")

            fout.write(fin.read())

def fix_init_tex(config):
    with open("akordy/init.tex", "r") as fin:
        with open(os.path.join(BUILD_DIR, "init.tex"), "w") as fout:
            fout.write(fin.readline())
            fout.write("\\usepackage{ifpdf}\n")

            fout.write(fin.read())

            if config.page_numbers:
                fout.write("\\pagestyle{plain}\n")

def copy_scripts():
    shutil.copy('akordy/maketoc.py', BUILD_DIR)
    shutil.copy('akordy/merge.py', BUILD_DIR)


def main():
    if len(sys.argv) < 2:
        cfg_file = "config.yml"
    else:
        cfg_file = sys.argv[1]

    prepare_build_directory()
    c = Config(cfg_file)
    songs = [ SongFile(os.path.join("zpevnik/nowtex", x)) for x in os.listdir("zpevnik/nowtex")]

    for s in songs:
        conf = c.get_config(s)

        if conf is None:
            continue

        transform(s.path, os.path.join(BUILD_DIR, "source"), conf)

    fix_init_tex(c)
    copy_scripts()

    subprocess.run(["python3", "maketoc.py", "source", "titleidx.sbx", "authidx.sbx"], cwd=BUILD_DIR)
    subprocess.run(["python3", "merge.py", "source", "zpevnik.tex"], cwd=BUILD_DIR)
    subprocess.run(["pdflatex", "zpevnik.tex"], cwd=BUILD_DIR)
    subprocess.run(["pdflatex", "zpevnik.tex"], cwd=BUILD_DIR)

if __name__ == "__main__":
    main()
