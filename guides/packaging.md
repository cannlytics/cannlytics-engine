# Packaging Cannlytics

Packaging Python modules and deploying them to [PyPI](https://pypi.org) is super easy.

1. [Test the package](#test).
2. [Install developer tools](#install).
3. [Publish the package](#publish).

## 1. Test the package <a name="test"></a>

First, it is recommended that you ensure that all tests pass with:

```bash
cd ./tests
pytest --disable-pytest-warnings
cd ../
```

## 2. Install developer tools <a name="install"></a>

Second, it is recommended to install the latest versions of `setuptools`, `wheel`, and `Twine` before each publish with:

```bash
pip install --user --upgrade setuptools wheel twine
```

## 3. Publish the package <a name="publish"></a>

Finally, when you are ready to publish, you can build the package from the same directory where `setup.py` is located with:

```bash
python setup.py sdist bdist_wheel
```

Next, you can run Twine to upload all of the archives under `dist`. If you are deploying to test, then run:

```bash
python -m twine upload --repository testpypi dist/*
```

When you are ready to deploy to production, then run:

```bash
python -m twine upload dist/*
```

You will be prompted for a username and password. For the username, use `__token__`. For the password, use your API key issued on [PyPI](https://pypi.org), including the *pypi-* prefix. On Windows, when entering your password, right click the taskbar, then select `Edit` > `Paste`, because other pasting methods do not work for this password field.

## Resources

- [Real Python Packaging Tutorial](https://realpython.com/pypi-publish-python-package/)
