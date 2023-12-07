FROM condaforge/miniforge3:23.3.1-1

ADD . /sky-atc

RUN conda install grpcio
RUN bash -c "pip install /sky-atc[runpod]"


CMD python -m sky_atc