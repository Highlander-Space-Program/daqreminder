# daqreminder

A bot that automatic pings daq members weekly for the daq meeting.

## Features

- No ping during break
- Start and end time for pinging (quarter ends = meeting time might change)
- Send custom discord webhook messages to ping members.

## Run

Make sure you have the [`uv`](https://docs.astral.sh/uv/getting-started/)
command installed on your machine.

- Copy and paste `config-example.yml`
- Rename the new `config-example.yml` file to `config.yml`
- Change the `config.yml` according to your needs.
- `uv venv`
- `uv sync`
- `uv run daqreminder`

## Environment variables

These are used to configure the logger used internally for debugging purposes.
There are two possible environment variables: `LOG_LEVEL` and `EXTRA_LOGGERS`.
`LOG_LEVEL` can have values of `info`, `warning`, `debug`, `error`, and
`trace`. `EXTRA_LOGGERS` are the library loggers that you want to see in
STDOUT, they will all use the same log level specified by `LOG_LEVEL`.
