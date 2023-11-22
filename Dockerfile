FROM condaforge/miniforge3:23.3.1-1

ADD . /sky-atc

RUN conda install grpcio
RUN pip install /sky-atc


CMD python -m sky_atc