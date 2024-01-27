from flask import Flask, render_template, request, redirect, url_for
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    input_path = "input.pdf"
    output_path = "output_compressed.pdf"

    with open(input_path, 'rb') as in_file:
        reader = PdfReader(in_file)
        writer = PdfWriter()

        for page in reader.pages:
            try:
                resources = page['/Resources']
                if '/XObject' in resources:
                    x_objects = resources['/XObject'].get_object()
                    for obj in x_objects:
                        if x_objects[obj]['/Subtype'] == '/Image':
                            x_objects[obj].update({
                                NameObject("/Filter"): NameObject("/DCTDecode"),
                                NameObject("/BitsPerComponent"): NameObject("/8"),
                                NameObject("/ColorTransform"): NameObject("/0")
                            })
            except KeyError:
                pass  # Ignore if '/Resources' or '/XObject' is not present
            writer.add_page(page)

        with open(output_path, 'wb') as out_file:
            writer.write(out_file)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
