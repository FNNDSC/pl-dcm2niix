# `pl-dcm2niix` _ChRIS_ Plugin 

[![Version](https://img.shields.io/docker/v/fnndsc/pl-dcm2niix?sort=semver)](https://hub.docker.com/r/fnndsc/pl-dcm2niix)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-dcm2niix)](https://github.com/FNNDSC/pl-dcm2niix/blob/main/LICENSE)
[![Build](https://github.com/FNNDSC/pl-dcm2niix/actions/workflows/build.yml/badge.svg)](https://github.com/FNNDSC/pl-dcm2niix/actions)

`pl-dcm2niix` is a _ChRIS_ _ds_ plugin wrapper around
[dcm2niix](https://github.com/rordenlab/dcm2niix).
It converts an input directory of DICOMs into an output
directory of NIFTI images.

[![chrisstore.co](https://github.com/FNNDSC/cookiecutter-chrisapp/blob/master/doc/assets/badge/light.png?raw=true)](https://chrisstore.co/plugin/pl-dcm2niix)

## Usage

`pl-dcm2niix` can run from [_ChRIS_](https://app.chrisproject.org/)
or locally on the command-line using [Apptainer](https://apptainer.org/).

```shell
singularity exec docker://fnndsc/pl-dcm2niix dcm2niixw input/ output/
```

A subset of the options from the original `dcm2niix` are available.

## Examples

Example datasets can be obtained from here:

https://github.com/DataCurationNetwork/data-primers/blob/master/Neuroimaging%20DICOM%20and%20NIfTI%20Data%20Curation%20Primer/neuroimaging-dicom-and-nifti-data-curation-primer.md#example-datasets

To convert DICOMs in `inputdir/` to NIFTIs in `outputdir/`,
without producing BIDs sidecar JSON (`-b n`), disable automatic
2D slice merge (`-m n`), compressed `.nii.gz` output (`-z y`):

```shell
singularity exec docker://fnndsc/pl-dcm2niix dcm2niixw -b n -m n -z y inputdir/ outputdir/
```
