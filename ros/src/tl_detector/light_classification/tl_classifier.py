from styx_msgs.msg import TrafficLight

import numpy as np
import cv2
import tensorflow as tf
import rospy

# Helper code
def load_image_into_numpy_array(image):
    return np.asarray(image, dtype="uint8")

VALID_TH = 0.1
TL_CLASS_NO = 10

class TLClassifier(object):
    def __init__(self):
        MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
        self.number_of_images = 0

        # Path to frozen detection graph. This is the actual model that is used for the object detection.
        PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

        self.model = None
        self.width = 0
        self.height = 0
        self.channels = 3

        # ref_url: https://github.com/tensorflow/models/issues/2788
        # LoadPATH_TO_CKPT a (frozen) Tensorflow model into memory
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            self.sess = tf.Session(graph=self.detection_graph)
            # Definite input and output Tensors for detection_graph
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')


    def init_classifier(self, model, width, height, channels=3):
        self.width = width
        self.height = height
        self.model = model
        self.channels = channels
        # necessary work around to avoid troubles with keras
        self.graph = tf.get_default_graph()

    def tl_light_classifier(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        resized = cv2.resize(image, (32,64))
        resized = resized / 255.; # Normalization
        # necessary work around to avoid troubles with keras
        with self.graph.as_default():
            predictions = self.model.predict(resized.reshape((1, 64, 32, self.channels)))
            color =  predictions[0].tolist().index(np.max(predictions[0]))
            tl = TrafficLight()
            tl.state = color
            return tl.state

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        # ref_url:https://github.com/tensorflow/models/issues/1773
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)

        with self.detection_graph.as_default():
            (boxes, scores, classes, num) = self.sess.run(
                [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
                feed_dict={self.image_tensor: image_np_expanded})

        boxes = np.squeeze(boxes)
        classes = np.squeeze(classes).astype(np.int32)
        scores = np.squeeze(scores)

        for idx, classID in enumerate(classes):
            if classID == TL_CLASS_NO:
                break

        tmp = (0, 0, 0, 0)
        # confidence threshold too low
        if scores[idx] < VALID_TH:
            return TrafficLight.UNKNOWN, tmp

        nbox = boxes[idx]

        height = image.shape[0]
        width = image.shape[1]

        box = np.array([nbox[0]*height, nbox[1]*width, nbox[2]*height, nbox[3]*width]).astype(int)

        tl_image = image[box[0]:box[2], box[1]:box[3]]
#        img_out = cv2.cvtColor(tl_image, cv2.COLOR_RGB2BGR)
#        cv2.imwrite('20180318_2_' + str(self.number_of_images) + '.jpg', img_out)
#        self.number_of_images += 1

        tl_s = self.tl_light_classifier(tl_image)
        return  tl_s, box
