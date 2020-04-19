from flask import Flask, send_file, request, abort
from io import BytesIO
from PIL import Image
import qrcode

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    version = 4
    border = 1
    box_size = 30
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )

    if not request.args.get('data'):
        return abort(400, 'data parameter missing')

    qr.add_data(request.args.get('data'))
    qr.make()
    img_io = BytesIO()
    qr_img = qr.make_image(fill_color="black")
    qr_img = qr_img.convert("RGB")

    width, height = qr_img.size

    logo_img = Image.open('logo_solid.png')
    logo_size = 450

    xmin = ymin = int((width / 2) - (logo_size / 2))
    xmax = ymax = int((width / 2) + (logo_size / 2))

    logo_img = logo_img.resize((xmax - xmin, ymax - ymin))

    qr_img.paste(logo_img, (xmin, ymin, xmax, ymax))

    qr_img = qr_img.convert(mode='P', palette=Image.ADAPTIVE)
    qr_img = qr_img.quantize(method=2)

    qr_img.save(img_io, 'PNG', optimize=True)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
