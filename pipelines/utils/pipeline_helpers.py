"""
This is a helper for all Azure ML Pipelines
"""
from azureml.core import Experiment
from azureml.core.runconfig import Environment, CondaDependencies  # type: ignore
from azureml.pipeline.core import Pipeline, PublishedPipeline  # type: ignore
from pipelines.utils.environment import set_environment
from pipelines.utils.compute import get_compute  # type: ignore
from settings.env_vars import COMPUTE_NAME, MAX_NODES, MIN_NODES, SCALE_DOWN, VM_SIZE


def pipeline_base(aml_workspace):
    """
    Gets AzureML artifacts: AzureML Workspace, AzureML Compute Tagret and AzureMl Run Config
    Returns:
        Workspace: a reference to the current workspace
        ComputeTarget: compute cluster object
        Environment: environment for compute instances
    """
    # Get Azure machine learning cluster

    aml_compute = get_compute(workspace=aml_workspace,
                              compute_name=COMPUTE_NAME,
                              vm_size=VM_SIZE,
                              min_nodes=MIN_NODES,
                              max_nodes=MAX_NODES,
                              scale_down=SCALE_DOWN)

    if aml_compute is not None:
      batch_env = set_environment()

    return aml_compute, batch_env


def submit_pipeline(workspace, pipeline):
    # Submit the pipeline to be run
    pipeline_run1 = Experiment(
        workspace, 'Compare_Models_Exp').submit(pipeline)
    pipeline_run1.wait_for_completion()


def publish_pipeline(aml_workspace, steps, pipeline_name,
                     build_id) -> PublishedPipeline:
    """
    Publishes a pipeline to the AzureML Workspace
    Parameters:
      aml_workspace (Workspace): existing AzureML Workspace object
      steps (list): list of PipelineSteps
      pipeline_name (string): name of the pipeline to be published
      build_id (string): DevOps Pipeline Build Id

    Returns:
        PublishedPipeline
    """
    train_pipeline = Pipeline(workspace=aml_workspace, steps=steps)
    train_pipeline.validate()
    published_pipeline = train_pipeline.publish(
        name=pipeline_name,
        description="Model training/retraining pipeline",
        version=build_id)
    print(
        f'Published pipeline: {published_pipeline.name} for build: {build_id}')

    return published_pipeline
