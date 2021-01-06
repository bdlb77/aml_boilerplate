#!/bin/bash

if [ "$#" -eq 0 ] || [ "$#" -eq 1 ]
then
  echo "USAGE: ./setup_aml_env.sh [\$RG_NAME] [\$AZURE_LOCATION]"
  exit 0
fi

export LC_ALL=C
export RG_NAME=$1
export AZURE_LOCATION=$2
export KEYVAULT_NAME=kv-$RG_NAME-$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
export STORAGE_KIND=BlobStorage
export STORAGE_NAME=storage$(echo $RG_NAME | tr -dc 'a-z')

echo 'Creating Resource Group'
export RESOURCE_GROUP=$(az group create \
  --name $RG_NAME \
  --location $AZURE_LOCATION \
  --query name -o tsv)

echo "Resource Group: $RESOURCE_GROUP created."


echo "Creating Key Vault"
export KEYVAULT_ID=$(az keyvault create \
  --name $KEYVAULT_NAME \
  --resource-group $RG_NAME \
  --location $AZURE_LOCATION \
  --query id -o tsv)

echo "Creating Storage Account"

export STORAGE_ID=$(az storage account create \
  --name $STORAGE_NAME \
  --resource-group $RG_NAME \
  --location $AZURE_LOCATION \
  --query id -o tsv)


echo "Create AML Workspace"
WORKSPACE_NAME="${RG_NAME}ws"

az ml workspace create \
  --workspace-name $WORKSPACE_NAME \
  --location $AZURE_LOCATION \
  --keyvault $KEYVAULT_ID \
  --storage-account $STORAGE_ID \
  --resource-group $RG_NAME

echo "Created AML Workspace"

export SUBSCRIPTION_ID=$(az account show --query id -o tsv)

echo "Creating .env file with secrets"
# Generate env file
cat .env.sample \
  | sed -e "s/{{WORKSPACE_NAME}}/$WORKSPACE_NAME/" \
  | sed -e "s/{{SUBSCRIPTION_ID}}/$SUBSCRIPTION_ID/" \
  | sed -e "s/{{RESOURCE_GROUP}}/$RESOURCE_GROUP/" \
> .env

echo "--- Good to go! ---"
