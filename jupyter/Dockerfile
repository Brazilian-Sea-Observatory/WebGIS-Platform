FROM jupyter/datascience-notebook

WORKDIR /home/jovyan/work

COPY ./requirements.txt ./requirements.txt

RUN conda update -n base conda
RUN conda install --file requirements.txt -y

USER root

CMD ["python", "netcdf_to_json.py"]

