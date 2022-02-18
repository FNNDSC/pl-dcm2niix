#!/usr/bin/env python

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from chris_plugin import chris_plugin
import subprocess as sp

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
parser.add_argument('-b', default='y', choices=('y', 'n', 'o'),
                    help='BIDS sidecar')
parser.add_argument('-d', default=5, choices=range(10), type=int,
                    help='directory search depth. Convert DICOMs in sub-folders of in_folder?')
parser.add_argument('-f', default='%f_%p_%t_%s', type=str,
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
    min_memory_limit='100Mi',
    min_cpu_limit='1000m',
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    cmd = (
        'dcm2niix',
        '-b', options.b,
        '-d', str(options.d),
        '-f', options.f,
        '-m', options.m,
        '-v', options.v,
        '-x', options.x,
        '-z', options.z,
        '-o', outputdir, inputdir
    )

    print(Gstr_title)
    print(f'Command: {" ".join(map(str, cmd))}')

    sp.run(cmd, check=True)


if __name__ == '__main__':
    main()
