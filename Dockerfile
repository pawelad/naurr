# syntax=docker/dockerfile:1.3
FROM python:3.12.6-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG UID=1000
ARG GID=1000

ENV USER="naurr"
ENV HOME="/home/$USER"
ENV APP_DIR="$HOME/app"
ENV VIRTUAL_ENV="$HOME/venv"

# Install system dependencies
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,sharing=locked,target=/var/lib/apt/lists \
    --mount=type=cache,sharing=locked,target=/var/cache/apt \
    apt-get update \
    && apt-get --no-install-recommends install -y \
      make

# Create a non root user
RUN groupadd --gid ${GID} $USER \
    && useradd --system --create-home --no-log-init \
      --uid ${UID} --gid ${GID} \
      --shell /bin/bash $USER

USER $USER
WORKDIR $APP_DIR

###########
# Builder #
###########
FROM base as builder

USER $USER

# Set up the virtualenv
RUN python -m venv --copies "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY --chown=$USER:$USER requirements/main.txt $APP_DIR/requirements/main.txt
RUN --mount=type=cache,uid=${UID},gid=${GID},target=$HOME/.cache \
    python -m pip install --no-deps -r requirements/main.txt

###########
#   Dev   #
###########
FROM builder as dev

# Install dev dependencies
COPY --chown=$USER:$USER requirements/dev.txt $APP_DIR/requirements/dev.txt
RUN --mount=type=cache,uid=${UID},gid=${GID},target=$HOME/.cache \
    python -m pip install --no-deps -r requirements/dev.txt

###########
#   App   #
###########
FROM base as app

# Copy virtualenv from builder
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the app
COPY --chown=$USER:$USER src/ $APP_DIR/src

# Collect static assets
RUN python src/manage.py collectstatic --noinput

# Run the app with `gunicorn`
EXPOSE 8000
ENTRYPOINT ["gunicorn", "--pythonpath=src", "--bind=0.0.0.0:8000", "--worker-tmp-dir=/dev/shm", "naurr.wsgi"]
