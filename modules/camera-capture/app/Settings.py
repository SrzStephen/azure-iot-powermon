from knobs import Knob

VERBOSE = Knob(env_name='VERBOSE', default=False, description="Show detailed logs and perf timers.")
VIDEO_PATH = Knob(env_name="VIDEO_PATH", default="/dev/video0",
                  description="Camera device path such as /dev/video0 or a test video file such as /TestAssets/myvideo.avi.")
IMAGE_PROCESSING_ENDPOINT = Knob(env_name="IMAGE_PROCESSING_ENDPOINT", default="/dev/video0",
                                 description="Service endpoint to send the frames to for processing. Example: 'http://face-detect-service:8080'. Leave empty when no external processing is needed.")
IMAGE_PROCESSING_PARAMS = Knob(env_name='IMAGE_PROCESSING_PARAMS', default="",
                               description="Query parameters to send to the processing service. Example: 'returnLabels': 'true'. Empty by default.")
SHOW_VIDEO = Knob(env_name='SHOW_VIDEO', default=False, description="Show the video in a windows")
LOOP_VIDEO = Knob(env_name='LOOP_VIDEO', default=False, description="If reading a video file, loop the video")
CONVERT_TO_GRAY = Knob(env_name='CONVERT_TO_GRAY', default=False,
                       description="Convert to grayscale before sending to an external process for processing")
RESIZE_WIDTH = Knob(env_name='RESIZE_WIDTH', default=0, description="Resize frame width in pixels, 0 for no resizing.")
RESIZE_HEIGHT = Knob(env_name='RESIZE_HEIGHT', default=0,
                     description="Resize frame height in pixels, 0 for no resizing.")
ANNOTATE = Knob(env_name='ANNOTATE', default=False,
                description="When showing the video in a window, it will annotate the frames with rectangles given by the image processing service.Rectangles should be passed in a json blob with a key containing the string rectangle, and a top left corner + bottom right corner or top left corner with width and height")
