import os
from dotenv import load_dotenv
from pathlib import Path


PROJECT_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent

env_file = Path.joinpath(PROJECT_ROOT, '.env')
load_dotenv(dotenv_path=env_file)
RESOURCE_GROUP = os.environ.get('RESOURCE_GROUP')
SUBSCRIPTION_ID = os.environ.get('SUBSCRIPTION_ID')

# Azure Credentials
WORKSPACE_NAME = os.environ.get('WORKSPACE_NAME')
# Compute Cluster Configuration
COMPUTE_NAME = "traincluster"
MIN_NODES = 1
MAX_NODES = 4
VM_SIZE = "Standard_D3_v2"
SCALE_DOWN = 300
