FROM mambaorg/micromamba:0.20.0

LABEL org.opencontainers.image.authors="Junel Solis, Image Data Team, Turku BioImaging"
LABEL org.opencontainers.image.url="https://bioimaging.fi"
LABEL org.opencontainers.image.source="https://github.com/turku-bioimaging/idt-texture-analysis"
LABEL org.opencontainers.image.title="Image Texture Analysis"

WORKDIR /code

COPY --chown=$MAMBA_USER:$MAMBA_USER ./environment-docker.yml /tmp/env.yml
COPY environment.yml measure.py texture.py /code/

RUN micromamba install -y -f /tmp/env.yml \
    && micromamba clean --all --yes

CMD [ "python", "measure.py" ]
