# get camera list
import logging
from datetime import datetime
from typing import List

import requests

from protect_archiver.dataclasses import Camera


def get_camera_list(session, connected=True) -> List[Camera]:
    cameras_uri = f"{session.authority}{session.base_path}/cameras"

    response = requests.get(
        cameras_uri,
        cookies={"TOKEN": session.get_api_token()},
        verify=session.verify_ssl,
    )
    if response.status_code != 200:
        print(f"Error while loading camera list: {response.status_code}")
        return []

    logging.info(f"Successfully retrieved data from {cameras_uri}")
    cameras = response.json()

    camera_list = []
    for camera in cameras:
        camera_list.append(
            Camera(
                id=camera["id"],
                name=camera["name"],
                recording_start=datetime.utcfromtimestamp(
                    camera["stats"]["video"]["recordingStart"] / 1000
                ),
            )
        )

    logging.info(
        "Cameras found:\n{}".format(
            "\n".join(f"- {camera.name} ({camera.id})" for camera in camera_list)
        )
    )

    return camera_list
