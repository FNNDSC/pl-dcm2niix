# Dockerfile for multi-arch "production" images.
# Before building this image, the conda environment and wheel must be built on-the-metal.

FROM docker.io/library/debian:trixie-slim

ARG TARGETPLATFORM
COPY ./envs/${TARGETPLATFORM} /opt/conda-env
ENV PATH=/opt/conda-env/bin:$PATH

RUN --mount=type=bind,source=./dist,target=/dist pip install --no-cache-dir /dist/pl_dcm2niix-*.whl

CMD ["dcm2niixw"]
