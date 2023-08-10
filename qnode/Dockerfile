FROM python:3.12.0b4-bookworm

ENV RYE_INSTALL_OPTION="-y"
ENV PATH="/root/.rye/shims:${PATH}"
RUN apt update -q \
    && apt install -y net-tools iputils-ping dnsutils iproute2 \
    && bash -c "curl -sSf https://rye-up.com/get | bash" 

WORKDIR /usr/app

RUN ls && rm -rf .venv