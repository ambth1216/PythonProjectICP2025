import numpy as np
import cv2 as cv

# Create a sample grayscale image (e.g., 100x100 pixels with a white square in the center)
image = np.zeros((100, 100), dtype=np.uint8)
cv.rectangle(image, (30, 30), (70, 70), 255, -1)  # Draw a white square

# Apply Canny edge detection
edges = cv.Canny(image, 50, 150)

# Display the result
cv.imshow("Edges", edges)
cv.waitKey(0)
cv.destroyAllWindows()
