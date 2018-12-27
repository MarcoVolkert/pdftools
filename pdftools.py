import os
from typing import List

import PyPDF2
import fpdf


def interlace(front_name: str, back_name: str, out_name: str):
    pdf_front = open(front_name, 'rb')
    pdf_back = open(back_name, 'rb')
    reader_front = PyPDF2.PdfFileReader(pdf_front)
    reader_back = PyPDF2.PdfFileReader(pdf_back)
    writer = PyPDF2.PdfFileWriter()

    num_pages = reader_front.numPages
    if not num_pages == reader_back.numPages:
        return

    for i in range(0, num_pages):
        print(i, num_pages, num_pages - i)
        writer.addPage(reader_front.getPage(i))
        writer.addPage(reader_back.getPage(num_pages - 1 - i))

    with open(out_name, "wb") as pdf_out:
        writer.write(pdf_out)

    pdf_front.close()
    pdf_back.close()


def interlace_per_dir(in_dir: str, out_dir: str):
    for (dirpath, dirnames, filenames) in os.walk(in_dir):
        for front_name, back_name in list(_group(filenames, 2)):
            out_name = os.path.join(out_dir, front_name + "_interlaced.pdf")
            front_name = os.path.join(in_dir, front_name)
            back_name = os.path.join(in_dir, back_name)
            interlace(front_name, back_name, out_name)


def merge(filenames: List[str], output: str):
    merger = PyPDF2.PdfFileMerger()

    for pdf in filenames:
        with open(pdf, 'rb') as f:
            merger.append(f)

    with open(output, 'wb') as f:
        merger.write(f)


def merge_per_dir(in_dir: str, out_dir: str):
    counter = 0

    for (dirpath, dirnames, filenames) in os.walk(in_dir):
        out_name = os.path.join(out_dir, "merged_%03d.pdf" % counter)
        filenames = [os.path.join(dirpath, filename) for filename in filenames]
        merge(filenames, out_name)
        counter += 1


def write_images(images: List[str], output: str):
    pdf = fpdf.FPDF()

    for image in images:
        pdf.add_page()
        pdf.image(image)
    pdf.output(output + ".pdf", "F")


def _group(lst, n):
    """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]

    Group a list into consecutive n-tuples. Incomplete tuples are
    discarded e.g.

    group(range(10), 3)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    """
    return zip(*[lst[i::n] for i in range(n)])
