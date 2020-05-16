# astros
Measuring the impact of the Astros' cheating during 2017

### Installation
Errors were initially encountered when trying to install `Theano`
because of the way `pyenv` installs Python.
```
libpython3.6m.a(ceval.o): relocation R_X86_64_PC32 against symbol
`_Py_NoneStruct' can not be used when making a shared object;
recompile with -fPIC.
```

Passing an additional flag to `pyenv` when installing Python resolved
the issue.
```
PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install --force 3.6.10
```
