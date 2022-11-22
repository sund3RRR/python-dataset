# python-dataset
A simple pyqt6 visualization of mathstat analysis (regression + correlation).
## Setting up 
### Cloning repository
```
git clone https://github.com/kabachoke/python-dataset
cd python-dataset
```
### Setting up virtual environment
```
python -m venv venv
venv\scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```
### Run
`python main.py`
## Convert ui to py
```pyuic6 -x form.ui -o form.py```
## Update requirements.txt
`pip freeze > requirements.txt`
