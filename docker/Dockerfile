################
# Stage: Build #
################

FROM python:3.8-slim AS build

ENV POETRY_VERSION=1.4.0

WORKDIR /src

# Export poetry dependencies to file
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml ./
RUN poetry export --without-hashes --format requirements.txt --output /src/requirements.txt

#####################
# Stage: Production #
#####################
FROM python:3.8-slim AS prod

ENV PYTHONPATH=/src

WORKDIR /src

# Copy requirements from build stage, and install them
COPY --from=build /src/requirements.txt . 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run server
EXPOSE ${PORT:-7071}

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7071", "--chdir", "src", "main:server"]
