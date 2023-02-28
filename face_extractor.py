import cv2
import os
import numpy as np
# Create the input and output directories if they don't exist
if not os.path.exists('inputs'):
    os.makedirs('inputs')
if not os.path.exists('outputs'):
    os.makedirs('outputs')
else:
    print("Removing files from the output directory...")
    # Remove all files from the output directory
    for filename in os.listdir('outputs'):
        os.remove(os.path.join('outputs', filename))

# Create a Haar Cascade Classifier object for face detection
face_cascade = cv2.CascadeClassifier('Face_cascade.xml')

ROI_pixels = 100

# Loop over each input file in the inputs directory
for input_filename in os.listdir('inputs'):
    print(f"Processing {input_filename}...")
    # Load the input image
    input_path = os.path.join('inputs', input_filename)
    image = cv2.imread(input_path)
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.16,minNeighbors=8,minSize=(25,25),flags=0) # scaleFactor=1.1, minNeighbors=3)
    # Loop over each face and create a resized version of it
    for (x, y, w, h) in faces:
        #print("Face detected !")
        # Define the new ROI by adding 100 pixels to the left, right, top and bottom of the original ROI
        roi_x1 = max(x - ROI_pixels, 0)
        roi_y1 = max(y - ROI_pixels, 0)
        roi_x2 = min(x + w + ROI_pixels, image.shape[1])
        roi_y2 = min(y + h + ROI_pixels, image.shape[0])
        # Extract the face region from the original image
        face = image[roi_y1:roi_y2, roi_x1:roi_x2]
        # Calculate the aspect ratio of the face region
        aspect_ratio = float(face.shape[1]) / float(face.shape[0])
        # Determine the maximum dimension of the resized face
        if aspect_ratio > 1:
            # Landscape orientation - set width to 512
            new_height = int(512 / aspect_ratio)
            new_width = 512
        else:
            # Portrait orientation - set height to 512
            new_width = int(512 * aspect_ratio)
            new_height = 512
        # Resize the face to the calculated size
        resized_face = cv2.resize(face, (new_width, new_height))
        # Create a new image with a black background and the desired size
        new_image = np.zeros((512, 512, 3), np.uint8)
        # Calculate the center position for the resized face in the new image
        center_x = int((512 - new_width) / 2)
        center_y = int((512 - new_height) / 2)
        # Copy the resized face into the center of the new image
        new_image[center_y:center_y+new_height, center_x:center_x+new_width] = resized_face
        # Save the resized face to the output directory
        output_filename = os.path.splitext(input_filename)[0] + '_' + str(x) + '_face.jpg'
        output_path = os.path.join('outputs', output_filename)
        cv2.imwrite(output_path, new_image)
