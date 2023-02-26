# Environment Setup



Using Conda

Create new environment with requirements installed

```
$ conda create --name <environment_name> --file requirements.txt
$ conda activate <environment_name>
$ pip install -r requirements.txt
```

Using venv

```
# create environment
$ python -m venv <environment_name>

# POSIX bash/zsh
$ activate <environment_name>/bin/activate

# Windows
$ <environment_name>\Scripts\activate.bat

$ pip install -r requirements.txt
```

Run Pipeline



```
$ python main.py
```