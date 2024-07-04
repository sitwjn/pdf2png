FROM python:3.9

ARG HOME_PATH
ENV ENV_HOME_PATH=$HOME_PATH

RUN pip install --upgrade pip setuptools; \
    pip install pdfplumber Flask waitress Flask-Markdown; \
    mkdir $HOME_PATH

ADD pdf2png.py README.md example.html $HOME_PATH

WORKDIR $HOME_PATH

ENTRYPOINT python pdf2png.py ${ENV_HOME_PATH}
