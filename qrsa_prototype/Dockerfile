FROM python:3.12.0b4-bookworm as base

ENV RYE_INSTALL_OPTION="-y"
ENV PATH="/root/.rye/shims:${PATH}"
RUN apt update -q \
    && apt install -y \
        net-tools iputils-ping dnsutils iproute2 tcpdump\
    && bash -c "curl -sSf https://rye-up.com/get | bash"

WORKDIR /usr/app

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=requirements.lock,target=requirements.lock \
    --mount=type=bind,source=requirements-dev.lock,target=requirements-dev.lock \
    --mount=type=bind,source=.python-version,target=.python-version \
    --mount=type=bind,source=README.md,target=README.md\
    --mount=type=bind,source=common,target=common \
    --mount=type=bind,source=controller,target=controller\
    --mount=type=bind,source=qnode,target=qnode \
    rye sync -f --no-lock \
    && echo PS1=\"'\[\e[1;34m\][\u@$(hostname -i)(base) \W]\\$ \[\e[m\]'\" >> ~/.bashrc


FROM base as controller

RUN apt update -q \
    && apt install -y \
        ca-certificates curl gnupg lsb-release nodejs npm \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt update  \
    && apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin \
    && bash -c "curl -sSf https://rye-up.com/get | bash" \
    &&  echo PS1=\"'\[\e[1;35m\][\u@$(hostname -i)(controller) \W]\\$ \[\e[m\]'\" > ~/.bashrc
