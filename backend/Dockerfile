FROM python:3.8-slim

ENV USER=process-miner
ENV HOME=/app

# install backend dependencies
ENV REQUIRED_PACKAGES="make graphviz"
RUN apt-get update && \
    apt-get install --no-install-recommends -y ${REQUIRED_PACKAGES} && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# prepare backend
ENV SRC_DIR=${HOME}/code
COPY . ${SRC_DIR}
WORKDIR ${SRC_DIR}
RUN make setup-prod-env

# set up and use non root user for running the backend
RUN useradd -md ${HOME} ${USER}
RUN chown -R ${USER}:${USER} ${HOME}

# run app
USER ${USER}
CMD [ "waitress-serve", "--port=5000", "--call", "process_miner:create_app" ]