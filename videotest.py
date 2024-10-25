import cv2
import os
import shutil

# Set input folder, output file name, and output folder




def compileFromImages(input_folder, output_path):   
    # Get the list of image files in the input folder
    image_files = os.listdir(input_folder)

    # Get the dimensions of the first image
    first_image_path = os.path.join(input_folder, image_files[0])
    first_image = cv2.imread(first_image_path)
    height, width, channels = first_image.shape

    # Set the output video dimensions, frame rate, and codec
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'v264')

    # Create a VideoWriter object
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Loop through each image file in the input folder and add it to the output video
    for image_file in image_files:
        # Read the image
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)
        
        # Resize the image to match the output video dimensions
        resized_image = cv2.resize(image, (width, height))
        
        # Write the image to the output video
        out.write(image)
        
        # Display the frame
        
        # Wait for a key event

    print('Processing Completed.')
    # Release the VideoWriter object and destroy all windows
    out.release()
    fpath = "./tempDuplicates/images"
    try:
        shutil.rmtree(fpath)
        print(f"Directory '{fpath}' and its contents have been deleted successfully.")
    except FileNotFoundError:
        print(f"Directory '{fpath}' not found.")
    except PermissionError:
        print(f"Permission denied to delete the directory '{fpath}'.")
    except Exception as e:
        print(f"Error occurred while deleting the directory: {e}")