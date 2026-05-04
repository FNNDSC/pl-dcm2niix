# `pl-dcm2niix` _ChRIS_ Plugin 

[![Version](https://img.shields.io/docker/v/fnndsc/pl-dcm2niix?sort=semver)](https://hub.docker.com/r/fnndsc/pl-dcm2niix)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-dcm2niix)](https://github.com/FNNDSC/pl-dcm2niix/blob/main/LICENSE)
[![Build](https://github.com/FNNDSC/pl-dcm2niix/actions/workflows/build.yml/badge.svg)](https://github.com/FNNDSC/pl-dcm2niix/actions)

`pl-dcm2niix` is a _ChRIS_ _ds_ plugin wrapper around
[dcm2niix](https://github.com/rordenlab/dcm2niix).
It converts an input directory of DICOMs into an output directory of NIFTI
images. Also, [`dcmdjpeg`](https://support.dcmtk.org/docs/dcmdjpeg.html) is
bundled for convenient handling of JPEG-compressed DICOM files.

## Usage

`pl-dcm2niix` can run from [_ChRIS_](https://app.chrisproject.org/)
or locally on the command-line using [Apptainer](https://apptainer.org/).

```shell
apptainer exec docker://fnndsc/pl-dcm2niix dcm2niixw input/ output/
```

A subset of the options from the original `dcm2niix` are available.

## Examples

Example datasets can be obtained from here:

https://github.com/DataCurationNetwork/data-primers/blob/main/Neuroimaging%20DICOM%20and%20NIfTI%20Data%20Curation%20Primer/neuroimaging-dicom-and-nifti-data-curation-primer.md#example-datasets

To convert DICOMs in `inputdir/` to NIFTIs in `outputdir/`,
without producing BIDs sidecar JSON (`-b n`), disable automatic
2D slice merge (`-m n`), compressed `.nii.gz` output (`-z y`):

```shell
apptainer exec docker://fnndsc/pl-dcm2niix dcm2niixw -b n -m n -z y inputdir/ outputdir/
```

Pre-process all `*.dcm` files using `dcmdjpeg` before running `dcm2niix`:

```shell
apptainer exec docker://fnndsc/pl-dcm2niix dcm2niixw --dcmdjpeg inputdir/ outputdir/
```

> [!TIP]
> The command `dcmdjpeg` is a no-op on already decoded files, i.e. it's okay to
> use `dcmdjpeg` when `inputdir/` contains a mix of JPEG-compressed and
> ordinary DICOM files.

