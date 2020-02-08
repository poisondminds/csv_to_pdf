import sys
import pdfrw
import os
import shutil

SEPARATOR = ","
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotations = template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                    )
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

if len(sys.argv) < 3:
    print("Usage: python3 filler.py <data_file> <template_file>")
    quit()

data_path = sys.argv[1]
template_path = sys.argv[2]

data_file = open(data_path, 'r')
fields = data_file.readline().strip().split(SEPARATOR)

if not os.path.isdir("output"):
    os.mkdir("output")

line_num = 2
while True:
    line = data_file.readline()
    if not line:
        break;
    item_data = line.strip().split(SEPARATOR)
    item_dict = {}
    for i in range(len(fields)):
        item_dict[fields[i]] = item_data[i]

    result_filename = 'output/' + str(line_num) + '.pdf'
    print("Writing " + result_filename)
    write_fillable_pdf(template_path, result_filename, item_dict)
    line_num+=1

data_file.close()
shutil.make_archive("output", "zip")
print("Done - output.zip created")
