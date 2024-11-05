FROM ubuntu:latest
LABEL authors="arjuna"

ENTRYPOINT ["top", "-b"]

RUN pip install --upgrade requests-html lxml

pip install lxml_html_clean
pip install lxml_html_clean
pip install --upgrade pip
pip list --outdated  # чтобы увидеть устаревшие пакеты

