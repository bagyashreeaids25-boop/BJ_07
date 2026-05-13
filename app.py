# app.py

import streamlit as st
from PIL import Image, ImageOps, ImageFilter
from io import BytesIO

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Document Scanner - Adobe Scan Style")

st.write(
    "Upload a document image, convert it to black & white, "
    "and download it as a PDF."
)

uploaded_file = st.file_uploader(
    "Upload a document image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Open image
    image = Image.open(uploaded_file)

    # Display original image
    st.subheader("Original Document")
    st.image(image, use_container_width=True)

    if st.button("Convert to Scan PDF"):

        # Convert to grayscale
        gray = ImageOps.grayscale(image)

        # Enhance sharpness using edge enhancement
        gray = gray.filter(ImageFilter.SHARPEN)

        # Convert to pure black & white
        threshold = 150
        bw = gray.point(lambda x: 255 if x > threshold else 0, mode='1')

        # Show processed image
        st.subheader("Scanned Black & White Document")
        st.image(bw, use_container_width=True)

        # Convert image to PDF
        pdf_buffer = BytesIO()

        # Convert to RGB because PDF does not support mode '1'
        pdf_image = bw.convert("RGB")

        pdf_image.save(pdf_buffer, format="PDF")

        pdf_buffer.seek(0)

        # Download button
        st.download_button(
            label="📥 Download PDF",
            data=pdf_buffer,
            file_name="scanned_document.pdf",
            mime="application/pdf"
        )
