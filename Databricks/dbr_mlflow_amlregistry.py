import azureml
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
import mlflow

workspace_name = "test-onelabpublic-registry" # "test-onlabprivdbr-aml"
workspace_location = "westeurope"
resource_group = "test-onelabprivate-rg"
subscription_id = "<<your subscription>>"

svc_pr = ServicePrincipalAuthentication(
tenant_id = "<<your tenant id>>",
service_principal_id = "<<your spn>>",
service_principal_password = "<<your spn password>>")

import os

os.environ["AZURE_TENANT_ID"] =  "<<your tenant id>>"
os.environ["AZURE_CLIENT_ID"] = "<<your spn>>"
os.environ["AZURE_CLIENT_SECRET"] = "<<your spn password>>"

from azure.ai.ml import MLClient

#ml_client = MLClient(
#    svc_pr, subscription_id, resource_group, workspace_name
#)

#azureml_tracking_uri = ml_client.workspace.get(
#    ml_client.registry_name
#).mlflow_tracking_uri

ml_client_registry = MLClient(credential=svc_pr,
                        registry_name="test-onelabpublic-registry",
                        registry_location="westeurope")
print(ml_client_registry)

mlflow_registry_uri = ml_client_registry.registries.get(
  name="test-onelabpublic-registry",
).mlflow_registry_uri

print(mlflow_registry_uri)

mlflow.set_tracking_uri(mlflow_registry_uri)

mlflow.set_experiment(experiment_name="public-test2")
