# ♻️ changes

[![Github Actions](https://github.com/michaeljoseph/changes/actions/workflows/tests.yml/badge.svg)](https://github.com/michaeljoseph/changes/actions/workflows/tests.yml)
[![Circle CI](https://circleci.com/gh/michaeljoseph/changes/tree/master.svg?style=svg&circle-token=773a0b46ffcd27626f0ff3bef788ffe96d47e473)](https://circleci.com/gh/michaeljoseph/changes/tree/master)
[![pypi version](https://img.shields.io/pypi/v/changes.svg)](https://pypi.python.org/pypi/changes)
[![# of downloads](https://img.shields.io/pypi/dw/changes.svg)](https://pypi.python.org/pypi/changes)
[![codecov.io](https://codecov.io/github/michaeljoseph/changes/coverage.svg?branch=master)](https://codecov.io/github/michaeljoseph/changes?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/michaeljoseph/changes/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/michaeljoseph/changes/?branch=master)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/michaeljoseph/changes?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

🎵 [Ch-ch-changes] 🎵

![changes](media/changes.png)

## ⚡️ Quickstart

Install `changes` with `pipx`:

```
pipx install changes
```

```bash
$ changes --help
Usage: changes [OPTIONS] COMMAND [ARGS]...

  Ch-ch-changes

Options:
  -V, --version  Show the version and exit.
  --verbose      Enables verbose output.
  --dry-run      Prints (instead of executing) the operations to be performed.
  -h, --help     Show this message and exit.

Commands:
  publish  Publishes a release
  stage    Stages a release
  status   Shows current project release status.
```

## 📺 Demo

<details>
  <summary>Expand</summary>
  <img
    src="media/demo.svg"
    alt="changes demo"/>
</details>

## 🛠 Development

Use the `Makefile` targets to `test`, `lint` and generate the `docs`:

```bash
$ make
ci               Continuous Integration Commands
clean            Remove Python file artifacts and virtualenv
docs             Generate documentation site
lint             Lint source
serve            Serve documentation site
test             Run tests
venv             Creates the virtualenv and installs requirements
```

[Ch-ch-changes]: http://www.youtube.com/watch?v=pl3vxEudif8