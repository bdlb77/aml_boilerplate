"""
A script to create and publish the training pipeline
We are running it as a module to solve import problems
"""
# TODO: Import types from AzureML (ComputeTarget, BatchEnv, AzureStorageBlob)
# type: ignore
from azureml.core import RunConfiguration, Workspace, Datastore  # type: ignore
from azureml.pipeline.core import Pipeline, PipelineData, PipelineParameter  # type: ignore
from azureml.data.data_reference import DataReference  # type: ignore
from azureml.pipeline.steps import PythonScriptStep  # type: ignore
from pipelines.utils.pipeline_helpers import (
  pipeline_base,
  submit_pipeline
)
from settings.env_vars import (
  RESOURCE_GROUP,
  SUBSCRIPTION_ID,
  WORKSPACE_NAME
)


def create_pipeline():
    """
    Creates a training pipeline to train audio model

    Returns:
        string: pipeline id
    """
    aml_workspace = Workspace.get(name=WORKSPACE_NAME,
                                  subscription_id=SUBSCRIPTION_ID,
                                  resource_group=RESOURCE_GROUP)

    print(aml_workspace)
    blob_ds = Datastore(aml_workspace, "workspaceblobstore")

    aml_compute, batch_env = pipeline_base(aml_workspace)

    print("Get pipeline steps")
    steps = pipeline_steps(aml_compute, blob_ds, batch_env)

    pipeline = Pipeline(workspace=aml_workspace, steps=[steps])

    submit_pipeline(aml_workspace, pipeline)


def pipeline_steps(aml_compute, blob_ds, batch_env) -> str:
    """
    Creates a training pipeline steps

    Parameters:
        aml_compute (ComputeTarget): a reference to compute
        blob_ds (DataStore): a reference to compute
        batch_env (Environment): a reference to environment object

    Returns:
        string: published pipeline id
    """

    data_dir = PipelineParameter(name="data_dir", default_value="data")
    root_dir = DataReference(
        datastore=blob_ds,
        data_reference_name="root_dir",
        mode="mount")


    train_step_config = RunConfiguration()
    train_step_config.environment = batch_env
    train = PythonScriptStep(
        name="train_step",
        script_name="pipelines/training_pipeline/steps/train.py",
        arguments=[
          "--root_dir", root_dir,
          "--data_dir", data_dir
        ],
        inputs=[root_dir],
        outputs=[],
        compute_target=aml_compute,
        runconfig=train_step_config,
        allow_reuse=False,
    )


    steps = [train]

    print(f"Returning {len(steps)} step[s]")
    return steps

# # TODO: Copy Data to Storage Account OR if --data folderpath is passed.. Copy that to Storage Account
