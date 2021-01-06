from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core import Environment
from settings.packages import (
  PIP_PACKAGES,
  CONDA_PACKAGES
)
# `compute_target` as defined in "Azure Machine Learning compute" section above

def set_environment():
  """Create Environment to run the script Step in.

  Returns
  -------
  Environment
      batch environment containing listed pip and conda packages.
  """
  # Add some packages relied on by data prep step
  batch_env = Environment(name="batch_environment")
  batch_conda_deps = CondaDependencies.create(
      conda_packages=CONDA_PACKAGES,
      pip_packages=PIP_PACKAGES,
      pin_sdk_version=False)
  batch_env.python.conda_dependencies = batch_conda_deps
  return batch_env
