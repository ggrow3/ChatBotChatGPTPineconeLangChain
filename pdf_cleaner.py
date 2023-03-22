
import PyPDF2
import re

# Put your PDF here
pdf_file = 'ARN13842-ATP_3-21.8-001-WEB-4.pdf'

# Open the input PDF file in read-binary mode
with open(pdf_file, 'rb') as input_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(input_file)

    # Create a PDF writer object
    pdf_writer = PyPDF2.PdfWriter()

    # Iterate over all pages in the PDF file
    for page_num in range(len(pdf_reader.pages)):
    #for page_num in range(20):
        # Get the current page object
        page =  pdf_reader.pages[page_num]

        # Extract the page content as a string
        page_text = page.extract_text()

        # Remove all binary characters from the page text
        clean_text = ''.join([char for char in page_text if ord(char) < 128])

        # Create a new page object with the clean text
        clean_page = PyPDF2.PageObject.create_blank_page(None, page.mediabox.width, page.mediabox.height)
        clean_page.merge_page(page)
        clean_page._data = clean_text.encode('utf-8')

        # Add the clean page to the PDF writer
        pdf_writer.add_page(clean_page)

    # Open the output PDF file in write-binary mode
    with open('output.pdf', 'wb') as output_file:
        # Write the output PDF file
        pdf_writer.write(output_file)

def remove_non_unicode(text):
    binary_pattern = '[^\x00-\x7F]'
    text = re.sub(binary_pattern, '', text)

    # Remove all non-Unicode characters using regular expressions
    pattern = '[^\u0000-\uD7FF\uE000-\uFFFF]'
    return re.sub(pattern, '', text)

# Open the PDF file in read-binary mode
with open('output.pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract text from each page and join them into a single string
    text = '\n'.join([pdf_reader._get_page(i).extract_text() for i in range(len(pdf_reader.pages))])

    text = remove_non_unicode(text)

# Open a text file in write mode and write the extracted text to it
with open('fieldmanual.txt', 'w') as txt_file:
    txt_file.write(str(text))