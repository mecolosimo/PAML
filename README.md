# PAML

A Python ARM64 (darwin/apple) Math Library.
The ARM64 code is designed for darwin/apple, the are several
different between darwin and linux code;
see [HelloSilicon](https://github.com/below/HelloSilicon).

Yes, Python can do this natively. This is just an excuss to try and
merge assembler code with Python. And maybe it might be faster.

## Quickstart

This uses [uv](https://github.com/astral-sh/uv) to manage the project.
Hopefully, I configured it correctly to build the assembly library that
is used.

### Build

I have not found a good way to do this, but to make the dylib you need to build it first and any time you make changes to the *\*.s* files:

```bash
uv run make
```

### Tests

This will run the tests (and build the dylib).

```python
./build_and_test.sh
```
