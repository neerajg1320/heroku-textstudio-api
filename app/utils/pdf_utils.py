import os

from app.utils.debug_utils import debug_log

def get_pdf_text(input_file_path):
    import pdftotext

    text = None
    try:
        with open(input_file_path, "rb") as f:
            pages = pdftotext.PDF(f)
        text = "\n\n".join(pages)
    except pdftotext.Error as e:
        print(e)

    return text

def read_text_from_pdf(input_file_path, output_file_path):
    text = get_pdf_text(input_file_path)

    if text is not None:
        with open(output_file_path, "w") as f:
          f.write(text)
    else:
        print(input_file_path + ": PDF read error")


def pdf_unlock(input_file_path, output_file_path, password):
    import pikepdf
    try:
        pdf = pikepdf.open(input_file_path, password)
        pdf.save(output_file_path)
    except pikepdf._qpdf.PasswordError as e:
        debug_log("Invalid Password")

def get_pdf_images(input_file_path, output_dir):
    from pdf2image import convert_from_path, convert_from_bytes
    debug_log("input_file_path={}  output_dir={}".format(input_file_path, output_dir))
    dirname = os.path.splitext(input_file_path)[0]
    os.makedirs(dirname, exist_ok=True)

    debug_log("Creating images for pdf pages in directory: {}".format(dirname))
    pil_images = convert_from_path(input_file_path)
    index = 1
    for image in pil_images:
        page_filename = "page_" + str(index) + ".jpg"
        debug_log(page_filename, location=False)
        image.save(os.path.join(dirname, page_filename))
        index += 1