<div align="center" style="text-align:center; margin-top:1rem; margin-bottom: 1rem;">
  <img style="height:180px" alt="" src="https://firebasestorage.googleapis.com/v0/b/cannlytics.appspot.com/o/public%2Fimages%2Flogos%2Fcannlytics_calyx_detailed.svg?alt=media&token=108fea9c-29a8-40ba-aced-65aef39611e9">
  <div style="margin-top:0.5rem;">
    <h3>Simple, easy, cannabis analytics.</h3>
  </div>

<https://cannlytics.com>

[![License: MIT](https://img.shields.io/badge/License-MIT-darkgreen.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/pypi/v/cannlytics.svg)](https://pypi.org/project/cannlytics)
[![Coverage Status](https://coveralls.io/repos/github/cannlytics/cannlytics-ai/badge.svg?branch=main)](https://coveralls.io/github/cannlytics/cannlytics-ai?branch=main)


</div>

🔥 Cannlytics is simple, easy-to-use, **end-to-end** cannabis analytics software designed to make your data and information accessible. We believe that everyone in the cannabis industry should be able to access their rich, valuable data quickly and easily and that you will be better off for it. The Cannlytics Engine comes with **batteries included**, but you are always welcome to supercharge your setup with modifications and custom components.

- [🚀 Installation](#installation)
- [👩‍🏫 Documentation](#documentation)
- [🗝️ Authentication, Data, and File Management](#development)
- [🧐 Traceability](#automation)
- [👩‍🔬 Testing](#testing)
- [🤝 Contributing](#contributing)
- [❤️ Support](#support)
- [🏛️ License](#license)

## 🚀 Installation <a name="installation"></a>

You can install the Cannlytics engine from [PyPI](https://pypi.org/project/cannlytics/).

```shell
pip install cannlytics
```

You can also simply clone the repository to get your hands on the Cannlytics source code.

```shell
git clone https://github.com/cannlytics/cannlytics-engine.git
```

## 🐱‍👓 Documentation <a name="documentation"></a>

Please refer to the [Cannlytics Developer Guide](https://docs.cannlytics.com/) for detailed information about the module.

## 🗝️ Authentication, Data, and File Management

Cannlytics leverages Firebase by default for a database, file storage, and authentication.

## 🧐 Traceability <a name="traceability"></a>

Cannlytics supports the [Metrc](https://api-ok.metrc.com/Documentation) API out-of-the-box with batteries included. Simply plug in (your API keys) and play.

Producer / processor workflow:

<img style="max-width:100%" width="540px" alt="" src="./samples/metrc_grower_workflow.png">

Lab workflow:

<img style="max-width:100%" width="540px" alt="" src="./samples/metrc_lab_workflow.png">

Retail workflow:

<img style="max-width:100%" width="540px" alt="" src="./samples/metrc_retail_workflow.png">

## 👩‍🔬 Testing <a name="testing"></a>

You can run tests with code coverage with `pytest`.

```
pytest --cov=ai tests/
```

## 🤝 Contributing <a name="contributing"></a>

Contributions are always welcome! You are encouraged to submit issues, functionality, and features that you want to be addressed. You can also develop your own new features, fix known issues, and add documentation, tests, and examples. Anyone is welcome to contribute anything. Please see the [contributing guide](https://docs.cannlytics.com/developers/contributing) for more information.

## ❤️ Support <a name="support"></a>

Cannlytics is made available with ❤️ and <a href="https://opencollective.com/cannlytics-company">your good will</a>. Please consider making a contribution to keep the good work coming. Thank you 🙏

🥞 Bitcoin donation address: 34CoUcAFprRnLnDTHt6FKMjZyvKvQHb6c6

## 🏛️ License <a name="license"></a>

```
Copyright (c) 2021 Cannlytics

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
