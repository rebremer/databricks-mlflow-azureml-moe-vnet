import azureml
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
import mlflow

workspace_name = "<<Azure ML Workspace name>>"
workspace_location = "westeurope"
resource_group = "<<your resource group>>"
subscription_id = "<<your subscription>>"

svc_pr = ServicePrincipalAuthentication(
tenant_id = "<<your tenant id>>",
service_principal_id = "<<your spn>>",
service_principal_password = "<<your spn password>>")

import os

os.environ["AZURE_TENANT_ID"] =  "<<your tenant id>>"
os.environ["AZURE_CLIENT_ID"] = "<<your spn>>"
os.environ["AZURE_CLIENT_SECRET"] = "<<your spn password>>"

# COMMAND ----------

azureml_tracking_uri = "<<URL to Azure ML workspace>>"
azureml_registry_uri = "<<URL to Azure ML registry>"
mlflow.set_tracking_uri(azureml_tracking_uri)
mlflow.set_registry_uri(azureml_registry_uri)

# COMMAND ----------

mlflow.set_experiment(experiment_name="20230919-public")

# COMMAND ----------

import pandas as pd

file_url = "https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data/heart.csv"
df = pd.read_csv(file_url)
df["thal"] = df["thal"].astype("category").cat.codes

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    df.drop("target", axis=1), df["target"], test_size=0.3
)

# COMMAND ----------

mlflow.xgboost.autolog()
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, recall_score

model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")

# COMMAND ----------

with mlflow.start_run() as run:
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    print("Recall: %.2f%%" % (recall * 100.0))

# COMMAND ----------

mlflow.register_model(
    model_uri=f"runs:/{run.info.run_id}/model", name="20230906-heartdisease-model"
)

# COMMAND ----------
# MlflowException: API request to https://westeurope.api.azureml.ms/mlflow/v2.0/subscriptions/2a8ece59-09e0-4a84-9124-e965b97f5d2c/resourceGroups/test-onelabprivate-rg/providers/Microsoft.MachineLearningServices/registries/test-onelabpublic-registry/api/2.0/mlflow/model-versions/create failed with exception HTTPSConnectionPool(host='westeurope.api.azureml.ms', port=443): Max retries exceeded with url: /mlflow/v2.0/subscriptions/2a8ece59-09e0-4a84-9124-e965b97f5d2c/resourceGroups/test-onelabprivate-rg/providers/Microsoft.MachineLearningServices/registries/test-onelabpublic-registry/api/2.0/mlflow/model-versions/create (Caused by ResponseError('too many 500 error responses'))
