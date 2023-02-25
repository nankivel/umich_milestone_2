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
$ python -m venv <environment_name>
$ activate <environment_name>/bin/activate
$ pip install -r requirements.txt
```

Run Pipeline

```
$ python main.py
```