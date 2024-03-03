# Use multi-stage build to optimize final image size
# Stage 1: Build environment
FROM alpine:3.19.1 as builder

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    python3 \
    python3-dev \
    py3-pip \
    libffi-dev \
    libxslt-dev \
    libxml2-dev \
    openssl-dev \
    tar \
    git
RUN echo $(python3 -c "import site; print(site.getsitepackages()[0])")
# Install Python and pip, and find the site-packages path
RUN PYTHON_SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])") && \
    echo "Python site-packages path: ${PYTHON_SITE_PACKAGES}" > /site_packages_path.txt

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt /requirements.txt
RUN rm /usr/lib/python3.11/EXTERNALLY-MANAGED
# Install Python dependencies
RUN pip3 install --no-cache-dir -r /requirements.txt

# Stage 2: Runtime environment
FROM alpine:3.19.1

# Environment variables
ENV INSTANCE_NAME=searxng \
    AUTOCOMPLETE= \
    BASE_URL= \
    MORTY_KEY= \
    MORTY_URL= \
    SEARXNG_SETTINGS_PATH=/etc/searxng/settings.yml \
    UWSGI_SETTINGS_PATH=/etc/searxng/uwsgi.ini

# Create user and group for searxng
ARG SEARXNG_GID=977
ARG SEARXNG_UID=977
RUN addgroup -g ${SEARXNG_GID} searxng && \
    adduser -u ${SEARXNG_UID} -D -h /usr/local/searxng -s /bin/sh -G searxng searxng

# Install runtime dependencies
RUN apk add --no-cache \
    ca-certificates \
    su-exec \
    python3 \
    py3-pip \
    libxml2 \
    libxslt \
    openssl \
    tini \
    uwsgi \
    uwsgi-python3 \
    brotli

# Set work directory
WORKDIR /usr/local/searxng

# Copy the Python site-packages path from the builder
RUN mkdir -p /usr/lib/python3.11/site-packages
# Copy Python site-packages from builder to runtime environment
COPY --from=builder /usr/lib/python3.11/site-packages /usr/lib/python3.11/site-packages

# Copy application code with correct permissions
COPY --chown=searxng:searxng dockerfiles ./dockerfiles
COPY --chown=searxng:searxng searx ./searx

# Precompile Python files
RUN su searxng -c "python3 -m compileall -q searx"

# Set entrypoint, expose port and define volume
ENTRYPOINT ["/sbin/tini", "--", "/usr/local/searxng/dockerfiles/docker-entrypoint.sh"]
EXPOSE 8080
VOLUME /etc/searxng

# Metadata
ARG GIT_URL=unknown
ARG SEARXNG_GIT_VERSION=unknown
ARG SEARXNG_DOCKER_TAG=unknown
ARG LABEL_DATE=
ARG LABEL_VCS_REF=
ARG LABEL_VCS_URL=
LABEL maintainer="searxng <${GIT_URL}>" \
      description="A privacy-respecting, hackable metasearch engine." \
      version="${SEARXNG_GIT_VERSION}" \
      org.label-schema.schema-version="1.0" \
      org.label-schema.name="searxng" \
      org.label-schema.version="${SEARXNG_GIT_VERSION}" \
      org.label-schema.url="${LABEL_VCS_URL}" \
      org.label-schema.vcs-ref=${LABEL_VCS_REF} \
      org.label-schema.vcs-url=${LABEL_VCS_URL} \
      org.label-schema.build-date="${LABEL_DATE}" \
      org.label-schema.usage="https://github.com/searxng/searxng-docker" \
      org.opencontainers.image.title="searxng" \
      org.opencontainers.image.version="${SEARXNG_DOCKER_TAG}" \
      org.opencontainers.image.url="${LABEL_VCS_URL}" \
      org.opencontainers.image.revision=${LABEL_VCS_REF} \
      org.opencontainers.image.source=${LABEL_VCS_URL} \
      org.opencontainers.image.created="${LABEL_DATE}" \
      org.opencontainers.image.documentation="https://github.com/searxng/searxng-docker"
