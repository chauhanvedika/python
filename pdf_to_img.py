import os
from pdf2image import convert_from_path

def convert_pdf_to_images(input_folder, output_folder, batch_size=10, dpi=300):
    # Get all PDF file paths from the input folder
    pdf_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    total_pdfs = len(pdf_paths)
    processed_pdfs = 0

    while processed_pdfs < total_pdfs:
        current_batch = pdf_paths[processed_pdfs:processed_pdfs + batch_size]
        
        for pdf_path in current_batch:
            try:
                # Convert PDF to images with specified DPI
                images = convert_from_path(pdf_path, dpi=dpi)
                
                # Save images to the output folder
                base_name = os.path.splitext(os.path.basename(pdf_path))[0]
                for i, image in enumerate(images):
                    image_filename = f"{base_name}_page_{i + 1}.png"
                    image_path = os.path.join(output_folder, image_filename)
                    image.save(image_path, 'PNG')
                    print(f"Saved {image_path}")

            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")

        processed_pdfs += batch_size

        # Ask user if they want to process the next batch
        if processed_pdfs < total_pdfs:
            user_input = input("Do you want to process the next batch of PDFs? (yes/no): ").strip().lower()
            if user_input != 'yes':
                break

if __name__ == "__main__":
    # Example usage
    input_folder = r"C:\Users\HP\Desktop\Study\Internship\MahaDBT-Doc\pfd"
    output_folder = r"C:\Users\HP\Desktop\Study\Internship\MahaDBT-Doc\image"
    
    convert_pdf_to_images(input_folder, output_folder, batch_size=10, dpi=300)
