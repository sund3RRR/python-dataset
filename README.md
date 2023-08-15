# python-dataset
A simple pyqt6 visualization of mathstat analysis (regression + correlation).

![image](https://github.com/sund3RRR/python-dataset/assets/73298492/0d3e5cb6-eb0e-4476-aa79-9fb9ca6dc4d5)

## Setting up 
### Cloning repository
```
git clone https://github.com/sund3RRR/python-dataset
cd python-dataset
```
### Setting up virtual environment
```
python -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
### Run
`python main.py`
## Convert ui to py
```pyuic6 -x form.ui -o form.py```
## Update requirements.txt
`pip freeze > requirements.txt`
