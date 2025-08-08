import fitz  # also known as PyMuPDF
import uuid
import os

# Function to extract text and images from PDF files
def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    image_metadata = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        full_text += page.get_text()

        image_count = 0
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]

            pdf_base = os.path.splitext(os.path.basename(pdf_path))[0]
            image_name = f"{pdf_base}_page{page_num+1}_img{image_count+1}.{ext}"
            image_count += 1

            # Get bounding box of image on page
            bbox = fitz.Rect(img[1], img[2], img[3], img[4])

            # Expand the box slightly above and below to extract nearby nearby caption for the image
            context_box = bbox + fitz.Rect(0, -50, 0, 50) 
            nearby_text = page.get_textbox(context_box)
            if not nearby_text:
                nearby_text = page.get_text().strip()
            else:
                nearby_text = nearby_text.strip()


            image_metadata[image_name] = {
                "bytes": image_bytes,
                "caption": nearby_text,
                "page": page_num + 1
            }

    return full_text, image_metadata
