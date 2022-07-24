import pdfkit as pdf
'''
options = {
  "enable-local-file-access": None or maybe ""
}'''
options = {
    "disable-local-file-access": ""
}
pdf_file='~/Documents/GymWeights/Print/trapbar.pdf'
pdf.from_file('trapbar copy.html', pdf_file)#, #options=options)
