from flask import Flask, send_file, request, abort, render_template
from io import BytesIO
from PIL import Image
from flask_weasyprint import HTML, render_pdf
import qrcode

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/qrcode', methods=['GET'])
def getQR():
    if not request.args.get('data'):
        return abort(400, 'data parameter missing')
    qrcode = generate_qr_code(request.args.get('data'))
    return send_file(qrcode, mimetype='image/png')


@app.route('/pdf', methods=['GET'])
def getPDF():
    if not request.args.get('data'):
        return abort(400, 'data parameter missing')
    if not request.args.get('title'):
        return abort(400, 'title parameter missing')

    text = request.args.get('text') if request.args.get('text') else ""

    html = render_template('qrpdf.html', title=request.args.get(
        'title'), qr_data=request.args.get('data'), text=text)
    return render_pdf(HTML(string=html))


def generate_qr_code(data):
    version = 4
    border = 1
    box_size = 30
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make()
    img_io = BytesIO()
    qr_img = qr.make_image(fill_color="black")
    qr_img = qr_img.convert("RGB")

    width, height = qr_img.size

    logo_img = Image.open('logo.png').convert("RGBA")
    logo_size = 450

    xmin = ymin = int((width / 2) - (logo_size / 2))
    xmax = ymax = int((width / 2) + (logo_size / 2))

    logo_img = logo_img.resize((xmax - xmin, ymax - ymin))

    qr_img.paste(logo_img, (xmin, ymin, xmax, ymax), logo_img)

    qr_img = qr_img.convert(mode='P', palette=Image.ADAPTIVE)
    qr_img = qr_img.quantize(method=2)

    qr_img.save(img_io, 'PNG', optimize=True)
    img_io.seek(0)
    return img_io


if __name__ == '__main__':
    app.run(debug=True)
