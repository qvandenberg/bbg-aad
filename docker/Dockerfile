# ARG WORKDIR="/aad_pricing"

################
# Stage: Base #
################
FROM python:3.8-slim AS python-base

ENV POETRY_VERSION=1.4.0 \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/.venv \
    WHEEL_PATH=dist/
ENV PATH="${WHEEL_PATH}:/root/.poetry/bin:/root/.local/bin:$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"
RUN pip install --upgrade pip

################
# Stage: Builder #
################
FROM python-base as builder

RUN pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.in-project true

COPY . .
RUN  poetry install --no-interaction --no-cache --compile --only main \
    && poetry build --format wheel

#####################
# Stage: Test #
# Provide the container to run tests
#####################

FROM python-base as tests

ENV TEST_RESULT_FOLDER=testResults 

RUN pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.in-project true \
    && mkdir TEST_RESULT_FOLDER

COPY pyproject.toml .

RUN  poetry install --no-interaction --no-cache 

WORKDIR /testRunner
# \
# && poetry run pytest tests --report-log=TEST_RESULT_FOLDER/results.log

#####################
# Stage: Production #
#####################
FROM python-base AS prod

COPY --from=builder ${WHEEL_PATH} ${WHEEL_PATH}
COPY --from=builder /applications/ /applications/

RUN pip install dist/*

EXPOSE ${PORT:-8050}
ENTRYPOINT [ "gunicorn"]

CMD ["--workers=2", "--threads=1", "-b 0.0.0.0:8050", "--chdir", "applications", "server:server"]
