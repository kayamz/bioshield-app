# import handPoseImage
# import os

# inputImage = os.path.dirname(os.path.realpath(__file__))+'/handSampleImage/vSelfie.jpg'
# handPoseImage.detect_fingerPoint(inputImage)

import blurFinger
import os

inputImage = os.path.dirname(os.path.realpath(__file__))+'/handSampleImage/selfie1.jpg'
blurFinger.Finger_blur(inputImage)
