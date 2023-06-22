from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2


def clarifai(image_path, clarifai_key):
    IMAGE_FILE_LOCATION = image_path

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    PAT = clarifai_key
    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id='clarifai', app_id='main')

    with open(IMAGE_FILE_LOCATION, "rb") as f:
        file_bytes = f.read()

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id='food-item-recognition',
            # version_id='1d5fd481e0cf4826aa72ec3ff049e044',  ## This is optional. Defaults to the latest model version.
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        return "None"

    # Since we have one input, one output will exist here.
    output = post_model_outputs_response.outputs[0]

    i = 0
    result = []
    for concept in output.data.concepts:
        i += 1
        result.append(concept.name)
        if i == 3:
            break

    return ", ".join(result)
