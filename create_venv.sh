
#!/bin/bash

# apt install python3.10-venv -y
# apt install python3.10-dev -y

python3 -m venv venv
source venv/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pylint
python3 -m pip install --upgrade black
python3 -m pip install --upgrade flake8
python3 -m pip install --upgrade isort

python3 -m pip install -r requirements.txt