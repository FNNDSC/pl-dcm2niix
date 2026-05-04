#!/usr/bin/env python

import os
import sys
from collections.abc import Sequence
import shlex
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
import subprocess as sp
from tempfile import TemporaryDirectory

from loguru import logger
from chris_plugin import chris_plugin, PathMapper

Gstr_title = r"""
       _           _                 _____       _ _
      | |         | |               / __  \     (_|_)
 _ __ | |______ __| | ___ _ __ ___  `' / /'_ __  _ ___  __
| '_ \| |______/ _` |/ __| '_ ` _ \   / / | '_ \| | \ \/ /
| |_) | |     | (_| | (__| | | | | |./ /__| | | | | |>  <
| .__/|_|      \__,_|\___|_| |_| |_|\_____/_| |_|_|_/_/\_\
| |
|_|            DICOM to NIFTI converter

"""

parser = ArgumentParser(description='ChRIS ds plugin wrapper around dcm2niix. '
                                    'Converts a directory of DICOM files to NIFTI.',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-j', '--dcmdjpeg', action='store_true',
                    help='Pre-process with dcmdjpeg to decode JPEG-compressed DICOM files')
parser.add_argument('-b', default='y', choices=('y', 'n', 'o'),
                    help='BIDS sidecar')
parser.add_argument('-c', default='', type=str,
                    help='comment stored in NIfTI aux_file (up to 24 characters)')
parser.add_argument('-d', default=5, choices=range(10), type=int,
                    help='directory search depth. Convert DICOMs in sub-folders of in_folder?')
parser.add_argument('-f', default='%p_%t_%s', type=str,
                    help='filename (%%a=antenna (coil) name, %%b=basename, %%c=comments, %%d=description, '
                         '%%e=echo number, %%f=folder name, %%g=accession number, %%i=ID of patient, '
                         '%%j=seriesInstanceUID, %%k=studyInstanceUID, %%m=manufacturer, %%n=name of patient, '
                         '%%o=mediaObjectInstanceUID, %%p=protocol, %%r=instance number, %%s=series number, '
                         '%%t=time, %%u=acquisition number, %%v=vendor, %%x=study ID; %%z=sequence name;)')
parser.add_argument('-m', default='2', choices=('n', 'y', '0', '1', '2'),
                    help='merge 2D slices from same series regardless of echo, exposure, etc. [no, yes, auto]')
parser.add_argument('-v', default='0', choices=('n', 'y', '0', '1', '2'),
                    help='verbose [no, yes, logorrheic]')
parser.add_argument('-x', default='n', choices=('y', 'n', 'i'),
                    help='crop 3D acquisitions')
parser.add_argument('-z', default='n', choices=('y', 'o', 'i', 'n', '3'),
                    help='gz compress images [y=pigz, o=optimal pigz, i=internal:miniz, n=no, 3=no,3D]')


@chris_plugin(
    parser=parser,
    title='dcm2niix',
    category='MRI Processing',
    min_memory_limit='2Gi',
    min_cpu_limit='1000m',
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(Gstr_title, flush=True)
    if options.dcmdjpeg:
        with TemporaryDirectory() as tempdir:
            tempdir = Path(tempdir)
            dcmdjpeg(inputdir, tempdir)
            dcm2niix(options, tempdir, outputdir)
    else:
        dcm2niix(options, inputdir, outputdir)


def dcmdjpeg(input_dir: Path, output_dir: Path):
    for input_file, output_file in PathMapper.file_mapper(input_dir, output_dir, glob='**/*.dcm'):
        _run(('dcmdjpeg', input_file, output_file))


def dcm2niix(options, inputdir, outputdir):
    _run((
        'dcm2niix',
        '-b', options.b,
        '-d', str(options.d),
        '-f', options.f,
        '-m', options.m,
        '-v', options.v,
        '-x', options.x,
        '-z', options.z,
        '-o', outputdir, inputdir
    ))


def _run(args: Sequence[str | os.PathLike]):
    logger.info(' '.join(map(shlex.quote, map(str, args))))
    proc = sp.run(args)
    if proc.returncode != 0:
        sys.exit(proc.returncode)


if __name__ == '__main__':
    main()
