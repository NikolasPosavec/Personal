from PIL import Image
import os

def images_to_pdf(image_paths, output_pdf):
    images = []
    
    for image_path in image_paths:
        img = Image.open(image_path)
        img = img.convert('RGB')  # Convert to RGB mode for PDF compatibility
        images.append(img)
    
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF saved as {output_pdf}")
    else:
        print("No valid images provided.")

if __name__ == "__main__":
    input_path = input("Enter the image file or folder path: ").strip()
    output_pdf = input("Enter the output PDF filename (including .pdf): ").strip()

    image_extensions = ('.png', '.jpg', '.jpeg')

    if os.path.isdir(input_path):
        # If it's a folder, get all images
        image_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.lower().endswith(image_extensions)]
        image_files.sort()  # Sort to maintain order
    elif os.path.isfile(input_path) and input_path.lower().endswith(image_extensions):
        # If it's a single file, use it directly
        image_files = [input_path]
    else:
        print("Invalid file or folder path.")
        exit(1)

    if image_files:
        images_to_pdf(image_files, output_pdf)
    else:
        print("No images found.")
