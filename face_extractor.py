import cv2
import os
import numpy as np
import argparse

# Create the argument parser
parser = argparse.ArgumentParser(description='Face detection and resizing')
parser.add_argument('--input', type=str, required=True, help='input directory path')
parser.add_argument('--output', type=str, required=True, help='output directory path')
parser.add_argument('--roi', type=int, default=100, help='number of pixels to add to the left, right, top and bottom of the face ROI')
parser.add_argument("--face-size", type=int, default=100, help="Minimum face detection size (default=100).")
parser.add_argument("--detection-quality", type=int, default=7, help="Face detection quality, higher is better quality. (default=7)")
parser.add_argument("--output-size", type=int, default=512, help="Image output size in pixels (default=512).")

args = parser.parse_args()

# Create the input and output directories if they don't exist
if not os.path.exists(args.input):
    os.makedirs(args.input)
if not os.path.exists(args.output):
    os.makedirs(args.output)
else:
    print("Removing files from the output directory...")
    # Remove all files from the output directory
    for filename in os.listdir(args.output):
        os.remove(os.path.join(args.output, filename))

# Create a Haar Cascade Classifier object for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Loop over each input file in the inputs directory
for input_filename in os.listdir(args.input):
    print(f"Processing {input_filename}...")
    # Load the input image
    input_path = os.path.join(args.input, input_filename)
    image = cv2.imread(input_path)
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.16,minNeighbors=args.detection_quality,minSize=(args.face_size,args.face_size),flags=0) # scaleFactor=1.1, minNeighbors=3)
    # Loop over each face and create a resized version of it
    for (x, y, w, h) in faces:
        #print("Face detected !")
        # Define the new ROI by adding the specified number of pixels to the left, right, top and bottom of the original ROI
        roi_x1 = max(x - args.roi, 0)
        roi_y1 = max(y - args.roi, 0)
        roi_x2 = min(x + w + args.roi, image.shape[1])
        roi_y2 = min(y + h + args.roi, image.shape[0])
        # Extract the face region from the original image
        face = image[roi_y1:roi_y2, roi_x1:roi_x2]
        # Calculate the aspect ratio of the face region
        aspect_ratio = float(face.shape[1]) / float(face.shape[0])
        # Determine the maximum dimension of the resized face
        if aspect_ratio > 1:
            # Landscape orientation - set width to 512
            new_height = int(args.output_size / aspect_ratio)
            new_width = args.output_size
        else:
            # Portrait orientation - set height to 512
            new_width = int(args.output_size * aspect_ratio)
            new_height = args.output_size
        # Resize the face to the calculated size
        resized_face = cv2.resize(face, (new_width, new_height))
        # Create a new image with a black background and the desired size
        new_image = np.zeros((args.output_size, args.output_size, 3), np.uint8)
        # Calculate the center position for the resized face in the new image
        center_x = int((args.output_size - new_width) / 2)
        center_y = int((args.output_size - new_height) / 2)
        # Copy the resized face into the center of the new image
        new_image[center_y:center_y+new_height, center_x:center_x+new_width] = resized_face

        output_filename = os.path.splitext(input_filename)[0] + '_' + str(x) + '_face.jpg'
        output_path = os.path.join(args.output, output_filename)
        cv2.imwrite(output_path, new_image)
