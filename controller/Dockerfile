FROM python:3.12.0b4-bookworm

ENV RYE_INSTALL_OPTION="-y"
ENV PATH="/root/.rye/shims:${PATH}"
RUN apt update -q \
    && apt install -y \
        net-tools iputils-ping dnsutils iproute2 \
        ca-certificates curl gnupg lsb-release tcpdump \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt update  \
    && apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin \
    && bash -c "curl -sSf https://rye-up.com/get | bash"

WORKDIR /usr/app
