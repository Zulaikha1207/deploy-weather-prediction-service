"""
DataPak deployment space manage script
"""
import yaml
import os
import sys
from pprint import pprint
import json
from ibm_watson_machine_learning import APIClient

with open("params.yaml") as config_file:
        config = yaml.safe_load(config_file)

TERRAFORM_OUTPUT = config['infrastructure']['terraform_output_path']

def authentication():
    print("Authenticating cloud account...\n")
    if os.getenv("ibm_cloud_key"):

        wml_credentials = {
            "url": config['infrastructure']['wml_url'],
            "apikey": os.environ.get("ibm_cloud_key"),
        }
        client = APIClient(wml_credentials)  # Connect to IBM cloud

        return client

    raise Exception("API_KEY environment variable not defined")


def terraform_output(terraform_path=TERRAFORM_OUTPUT):

    output = dict(json.load(open(terraform_path)))["outputs"]

    cos_crn = output["cos_crn"]["value"]
    wml_crn = output["wml_crn"]["value"]["crn"]
    wml_name = output["wml_crn"]["value"]["resource_name"]

    state = {"cos_crn": cos_crn, "wml_name": wml_name, "wml_crn": wml_crn}
    #print('Collecting info about created COS and WML instances...\n')
    #print(state)
    return state


def create_deployment_space(client, cos_crn, wml_name, wml_crn, space_name="default", description=""):
    print("Creating deployment space..\n")
    metadata = {
        client.spaces.ConfigurationMetaNames.NAME: space_name,  ## Project info
        client.spaces.ConfigurationMetaNames.DESCRIPTION: description,
        client.spaces.ConfigurationMetaNames.STORAGE: {
            "type": "bmcos_object_storage",
            "resource_crn": cos_crn,
        },
        client.spaces.ConfigurationMetaNames.COMPUTE: {  ## Project compute instance (WML)
            "name": wml_name,
            "crn": wml_crn,
        },
    }

    space_details = client.spaces.store(meta_props=metadata)  # Create a space
    return space_details


def update_deployment_space(client, new_name, space_id):
    print("Updating deployment space..\n")
    metadata = {client.spaces.ConfigurationMetaNames.NAME: new_name}

    space_details = client.spaces.update(space_id, changes=metadata)
    return space_details

def delete_deployment_space(client, space_id):
    print("Deleting deployment space..\n")
    client.spaces.delete(space_id)


def list_deployment_space(client):
    print("List of deployment spaces..\n")
    spaces = client.spaces.list()
    print(spaces)


def describe_deployment_space(client, space_id):
    print("Details about the deployment space..\n")
    info = client.spaces.get_details(space_id)
    pprint(info)


def help():

    print(
        """
        datapak_config.py [options] 
        create  
        update  
        delete  
        list    
        describe
        """
    )


if __name__ == "__main__":

    client = authentication()

    args = sys.argv[1:]

    if len(args) >= 1:
        action = args[0]

        if action == "create":

            infos = terraform_output()
            if len(args) == 2:
                space_name = args[1]
                space = create_deployment_space(
                    client,
                    infos["cos_crn"],
                    infos["wml_name"],
                    infos["wml_crn"],
                    space_name,
                )

            elif len(args) > 2:
                space_name = args[1]
                description = args[2]
                space = create_deployment_space(
                    client,
                    infos["cos_crn"],
                    infos["wml_name"],
                    infos["wml_crn"],
                    space_name,
                    description,
                )

            print(space)

        elif action == "update":

            try:
                new_name = args[1]
                space_id = args[2]
            except:
                raise Exception("Missing arguments")

            space = update_deployment_space(client, new_name, space_id)
            print(space)

        elif action == "delete":
            try:
                space_id = args[1]
            except:
                raise Exception("Missing space_id")

            delete_deployment_space(client, space_id)

        elif action == "list":
            list_deployment_space(client)

        elif action == "describe":

            try:
                space_id = args[1]
            except:
                raise Exception("Missing space_id")

            describe_deployment_space(client, space_id)

        else:
            help()

    else:
        help()