import os
import argparse


parser = argparse.ArgumentParser(description="Compress PDF files using Ghostscript.")
parser.add_argument(
    "-i",
    "--input",
    type=str,
    default="inputs",
    help="Input folder containing PDF files (default: 'inputs')",
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="outputs",
    help="Output folder to save compressed PDFs (default: 'outputs')",
)
parser.add_argument(
    "-r",
    "--resolution",
    type=int,
    default=30,
    help="Image resolution in DPI (default: 30)",
)

args = parser.parse_args()
input_folder = args.input
output_folder = args.output
image_resolution = args.resolution


os.makedirs(output_folder, exist_ok=True)

pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]

if not pdf_files:
    print("🚨 No PDFs found in the folder:", input_folder)
else:
    print(f"📂 {len(pdf_files)} PDF files found. Compression starting...")

    for pdf_file in pdf_files:
        input_pdf = os.path.join(input_folder, pdf_file)
        output_pdf = os.path.join(
            output_folder, pdf_file.replace(".pdf", "_compressed.pdf")
        )

        command = f"""
        gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
           -dPDFSETTINGS=/screen \
           -dNOPAUSE -dQUIET -dBATCH \
           -dDetectDuplicateImages=true -dCompressFonts=true \
           -dDownsampleColorImages=true -dColorImageDownsampleType=/Bicubic -dColorImageResolution={image_resolution} \
           -dGrayImageDownsampleType=/Bicubic -dGrayImageResolution={image_resolution} \
           -dMonoImageDownsampleType=/Bicubic -dMonoImageResolution={image_resolution} \
           -dColorImageCompression=/DCTEncode -dGrayImageCompression=/DCTEncode \
           -dMonoImageCompression=/CCITTFaxEncode \
           -sOutputFile="{output_pdf}" "{input_pdf}"
        """

        print(f"⚙️  Compressing: {pdf_file} -> {output_pdf}")

        os.system(command)

    print("✅ All PDFs have been successfully compressed and saved in:", output_folder)
