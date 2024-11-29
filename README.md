# bfabric-app-template
Template Application for Bfabric Webapp Concept (written in Python3) 

## Deployment 

1) Fork the Repo 

2) Clone your Repo

``` 
git clone https://github.com/your/bfabric-app-template/fork.git && cd bfabric-app-template
```
3) Set up virtual environment:

For using virtualenv: 
``` 
python3 -m venv my_app_1
source my_app_1/bin/activate
```

For using conda: 

```
conda create -n my_app_1 pip
conda activate my_app_1
```

For using mamba: 
```
mamba create -n my_app_1 pip
conda activate my_app_1
```

4) Install remaining dependencies:

```
pip install -r requirements.txt
``` 

5) Create a PARAMS.py file with your host and port!

CONFIG_FILE_PATH specifies the path to the configuration file containing credentials for the power user. This is essential for managing API logging and accessing backend systems with the required permissions. The application uses this path to authenticate and perform operations as a power user.

```
# PARAMS.py
HOST = "0.0.0.0"
PORT = 8050
DEV = False
CONFIG_FILE_PATH = "~/.bfabricpy.yml"
```

6) Run the application 

```
python3 index.py
```

7) Check it out! 

Visit http://localhost:8050 to see your site in action.
