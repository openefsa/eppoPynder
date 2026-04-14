# eppoPynder <img src="https://raw.githubusercontent.com/openefsa/eppoPynder/main/media/logo.png" height="140" align="right">

[![Lifecycle: stable](https://img.shields.io/badge/lifecycle-stable-brightgreen.svg)](https://lifecycle.r-lib.org/articles/stages.html#stable) [![codecov](https://codecov.io/gh/openefsa/eppoPynder/branch/main/graph/badge.svg?token=6U3TL9T27T)](https://codecov.io/gh/openefsa/eppoPynder)

## Overview

**eppoPynder** provides a Python interface to the public APIs of the **European
and Mediterranean Plant Protection Organization (EPPO)** database.
The package facilitates access to a wide range of pest-related information
collected and maintained by EPPO, allowing users to query, retrieve, and
process this data directly from Python.

The package is intended for researchers, analysts, and practitioners in plant
protection who require convenient programmatic access to EPPO data.

## Installation

### From PyPi

```
pip install eppoPynder
```

### Development version

To install the latest development version:

```
pip install git+https://github.com/openefsa/eppoPynder.git
```

## Requirements

An active internet connection is required, as the package communicates with
EPPO's online services to fetch and process data.

## Usage

Once installed, load the package as usual:

```python
from eppopynder import *
```

Basic usage examples and full documentation are available in the package
[guide](docs/guide.md).

## Authors and maintainers

- **Lorenzo Copelli** (author, [ORCID](https://orcid.org/0009-0002-4305-065X)).
- **Dayana Stephanie Buzle** (author, [ORCID](https://orcid.org/0009-0003-2990-7431)).
- **Rafael Vieira** (author, [ORCID](https://orcid.org/0009-0009-0289-5438)).
- **Agata Kaczmarek** (author, [ORCID](https://orcid.org/0000-0002-7463-5821)).
- **Luca Belmonte** (author, maintainer, [ORCID](https://orcid.org/0000-0002-7977-9170)).

## Links

- **Homepage**: [GitHub](https://github.com/openefsa/eppoPynder).
- **Bug Tracker**: [Issues on GitHub](https://github.com/openefsa/eppoPynder/issues).
- **EPPO Database**: [https://gd.eppo.int](https://gd.eppo.int).
