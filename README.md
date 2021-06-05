# ♻️ changes

[![Travis CI](https://travis-ci.org/michaeljoseph/changes.svg?branch=master)](https://travis-ci.org/michaeljoseph/changes)
[![Circle CI](https://circleci.com/gh/michaeljoseph/changes/tree/master.svg?style=svg&circle-token=773a0b46ffcd27626f0ff3bef788ffe96d47e473)](https://circleci.com/gh/michaeljoseph/changes/tree/master)
[![Appveyor CI](https://ci.appveyor.com/api/projects/status/xy60i95qy7s83o91/branch/master?svg=true)](https://ci.appveyor.com/project/michaeljoseph/changes/branch/master)
[![pypi version](https://img.shields.io/pypi/v/changes.svg)](https://pypi.python.org/pypi/changes)
[![# of downloads](https://img.shields.io/pypi/dw/changes.svg)](https://pypi.python.org/pypi/changes)
[![codecov.io](https://codecov.io/github/michaeljoseph/changes/coverage.svg?branch=master)](https://codecov.io/github/michaeljoseph/changes?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/michaeljoseph/changes/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/michaeljoseph/changes/?branch=master)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/michaeljoseph/changes?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

:musical_note: [Ch-ch-changes](http://www.youtube.com/watch?v=pl3vxEudif8) :musical_note:

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

Use <code>[tox]</code> to `test`, `lint` and generate the `docs`:

```bash
$ pip install -r requirements.txt

$ tox -av
...
default environments:
lint            -> pre-commit with black, flake8, isort
test            -> pytests
safety          -> security check with safety
docs            -> mkdocs and pdoc3
package         -> builds source and wheel distributions

additional environments:
report-coverage -> codecov and scrutinizer integration
```

[tox]: https://tox.readthedocs.io/en/latest/