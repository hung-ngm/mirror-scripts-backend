FROM python:3.11.4-slim-bullseye as install-browser

RUN apt-get update \
    && apt-get install -y \
    chromium=114.* chromium-driver=114.* \
    && chromium --version && chromedriver --version

FROM install-browser as mirror-scripts-install

ENV PIP_ROOT_USER_ACTION=ignore

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

FROM mirror-scripts-install AS mirror-scripts

RUN useradd -ms /bin/bash mirror-scripts \
    && chown -R mirror-scripts:mirror-scripts /usr/src/app

USER mirror-scripts

COPY --chown=mirror-scripts:mirror-scripts ./ ./

EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
