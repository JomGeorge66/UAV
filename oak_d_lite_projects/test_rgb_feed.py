import depthai as dai
import cv2

# Create a pipeline
pipeline = dai.Pipeline()

# Define a source for the RGB camera
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(640, 480)  # Set resolution
cam_rgb.setInterleaved(False)
cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

# Create an XLink output to get the camera data to the host
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

# Connect to the device and start the pipeline
with dai.Device(pipeline) as device:
    # Get the output queue
    rgb_queue = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    print("Press 'q' to quit.")
    while True:
        # Get the latest frame from the queue
        in_rgb = rgb_queue.get()
        frame = in_rgb.getCvFrame()

        # Display the frame
        cv2.imshow("RGB Feed", frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cv2.destroyAllWindows()
