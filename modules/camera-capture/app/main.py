# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import os
import random
import sys
import time

import iothub_client
# pylint: disable=E0611
# Disabling linting that is not supported by Pylint for C extensions such as iothub_client. See issue https://github.com/PyCQA/pylint/issues/1955
from iothub_client import (IoTHubModuleClient, IoTHubClientError, IoTHubError,
                           IoTHubMessage, IoTHubMessageDispositionResult,
                           IoTHubTransportProvider)
import CameraCapture
from CameraCapture import CameraCapture
import click
from . import Settings

# global counters
SEND_CALLBACKS = 0


def send_to_Hub_callback(strMessage):
    message = IoTHubMessage(bytearray(strMessage, 'utf8'))
    hubManager.send_event_to_output("output", message, 0)


# Callback received when the message that we're forwarding is processed.
def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    SEND_CALLBACKS += 1


class HubManager(object):

    def __init__(
            self,
            messageTimeout,
            protocol,
            verbose):
        '''
        Communicate with the Edge Hub

        :param int messageTimeout: the maximum time in milliseconds until a message times out. The timeout period starts at IoTHubClient.send_event_async. By default, messages do not expire.
        :param IoTHubTransportProvider protocol: Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
        :param bool verbose: set to true to get detailed logs on messages
        '''
        self.messageTimeout = messageTimeout
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)
        self.client.set_option("messageTimeout", self.messageTimeout)
        self.client.set_option("product_info", "edge-camera-capture")
        if verbose:
            self.client.set_option("logtrace", 1)  # enables MQTT logging

    def send_event_to_output(self, outputQueueName, event, send_context):
        self.client.send_event_async(outputQueueName, event, send_confirmation_callback, send_context)

@click.command()
@click.option("--videoPath", default=Settings.VIDEO_PATH(), description=Settings.VIDEO_PATH.description())
@click.option("--endpoint", default=Settings.IMAGE_PROCESSING_ENDPOINT(),
              description=Settings.IMAGE_PROCESSING_ENDPOINT.description())
@click.option("--imageParams", default=Settings.IMAGE_PROCESSING_PARAMS(),
              description=Settings.IMAGE_PROCESSING_PARAMS.description())
@click.option("--showVideo", default=Settings.SHOW_VIDEO(), description=Settings.SHOW_VIDEO.description(),type=bool)
@click.option("--verbose", default=Settings.VERBOSE(), description=Settings.VERBOSE.description(),type=bool)
@click.option("--loopVideo", default=Settings.LOOP_VIDEO(), description=Settings.LOOP_VIDEO.description(),type=bool)
@click.option("--convertToGray", default=Settings.CONVERT_TO_GRAY(), description=Settings.CONVERT_TO_GRAY.description(),type=bool)
@click.option("--resizeWidth", default=Settings.RESIZE_WIDTH(), description=Settings.RESIZE_WIDTH.description(),type=int)
@click.option("--resizeHeight", default=Settings.RESIZE_HEIGHT(), description=Settings.RESIZE_HEIGHT.description(),type=int)
@click.option("--annotate", default=Settings.ANNOTATE(), description=Settings.ANNOTATE.description(),type=bool)
def main(
        videoPath,
        imageProcessingEndpoint,
        imageProcessingParams,
        showVideo,
        verbose,
        loopVideo,
        convertToGray,
        resizeWidth,
        resizeHeight,
        annotate
):
    try:
        print("\nPython %s\n" % sys.version)
        print("Camera Capture Azure IoT Edge Module. Press Ctrl-C to exit.")
        try:
            global hubManager
            hubManager = HubManager(10000, IoTHubTransportProvider.MQTT, verbose)
        except IoTHubError as iothub_error:
            print("Unexpected error %s from IoTHub" % iothub_error)
            return
        with CameraCapture(videoPath, imageProcessingEndpoint, imageProcessingParams, showVideo, verbose, loopVideo,
                           convertToGray, resizeWidth, resizeHeight, annotate, send_to_Hub_callback) as cameraCapture:
            cameraCapture.start()
    except KeyboardInterrupt:
        print("Camera capture module stopped")


if __name__ == '__main__':
    main()