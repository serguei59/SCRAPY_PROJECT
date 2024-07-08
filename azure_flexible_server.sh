# load environnements variables from .env
set -o allexport
source .env
set +o allexport

#creation gpe de ressources
az group create \
    --name $DBSERVER_RESOURCE_GROUP \
    --location $LOCATION



#creation d'une instance de serverflexible postgresql
az postgres flexible-server create \
    --admin-user $DB_USERNAME \
    --admin-password $DBSERVER_PASSWORD \
    --database-name $DB_NAME \
    --location $LOCATION \
    --resource-group $DBSERVER_RESOURCE_GROUP \
    --name $DBSERVER_NAME