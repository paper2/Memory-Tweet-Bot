from google.cloud import secretmanager
import logging
import os


def accessSecretVersion(project_id, secret_id, version_id):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    payload = response.payload.data.decode("UTF-8")
    return payload


def addSecretVersion(project_id, secret_id, payload):
    """
    payloadでシークレットに新しいバージョンを追加する。

    Returns
    -------
    version_id : int
        作成したversionのid。
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent secret.
    parent = client.secret_path(project_id, secret_id)

    # Convert the string payload into a bytes. This step can be omitted if you
    # pass in bytes instead of a str for the payload argument.
    payload = payload.encode("UTF-8")

    # Add the secret version.
    response = client.add_secret_version(
        request={
            "parent": parent,
            "payload": {"data": payload},
        }
    )

    # Print the new secret version name.
    logging.info("Added secret version: {}".format(response.name))

    version_id = os.path.basename(response.name)
    return int(version_id)


def destroy_secret_version(project_id, secret_id, version_id):
    """
    与えられたsecret versionを削除。
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Destroy the secret version.
    response = client.destroy_secret_version(request={"name": name})

    logging.info("Destroyed secret version: {}".format(response.name))
