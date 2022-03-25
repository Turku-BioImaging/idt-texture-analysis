FROM continuumio/miniconda3:4.10.3p0-alpine

LABEL org.opencontainers.image.authors="Junel Solis, Image Data Team, Turku BioImaging"
LABEL org.opencontainers.image.url="https://bioimaging.fi"
LABEL org.opencontainers.image.source="https://github.com/turku-bioimaging/idt-texture-analysis"
LABEL org.opencontainers.image.title="Image Texture Analysis"

WORKDIR /code

RUN addgroup -S pythonuser && adduser -S pythonuser -G pythonuser \
    && chown -R pythonuser:pythonuser /opt/conda 

COPY environment.yml measure.py texture.py /code/
RUN chmod o=rx environment.yml measure.py texture.py

USER pythonuser

RUN conda env create -f environment.yml && conda clean --all

ENV PATH /opt/conda/envs/idt-texture-analysis/bin:$PATH
RUN /bin/bash -c "source activate idt-texture-analysis"

CMD [ "python", "measure.py" ]
