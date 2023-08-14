FROM python:3.12.0b4-bookworm

ENV RYE_INSTALL_OPTION="-y"
ENV PATH="/root/.rye/shims:${PATH}"
RUN apt update -q \
    && apt install -y net-tools iputils-ping dnsutils iproute2 \
    && bash -c "curl -sSf https://rye-up.com/get | bash"


# COPY ./pyproject.toml ./usr/app/
# COPY ./README.md ./usr/app/
# COPY ./requirements.lock ./usr/app/
# COPY ./requirements-dev.lock ./usr/app/
# COPY ./.python-version ./usr/app/

WORKDIR /usr/app

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=requirements.lock,target=requirements.lock \
    --mount=type=bind,source=requirements-dev.lock,target=requirements-dev.lock \
    --mount=type=bind,source=.python-version,target=.python-version \
    --mount=type=bind,source=README.md,target=README.md\
    --mount=type=bind,source=common,target=common \
    rye sync --no-lock
