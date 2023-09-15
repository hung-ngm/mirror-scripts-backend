FROM python:3.11.4-slim-bullseye as install-browser

RUN apt-get update \
    && apt-get satisfy -y \
    "chromium, chromium-driver (>= 115.0)" \
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
CMD uvicorn main:app --host 0.0.0.0 --port $PORT --ws-ping-interval 600 --ws-ping-timeout 1200 --timeout-keep-alive 1800
