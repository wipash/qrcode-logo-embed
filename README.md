Setup:
---
```
apt-get install libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
pipenv install --dev
```

Run:
---
```
pipenv run python app.py
```

Use:
* Replace logo.png with your own square logo
* Generate a QR code: `http://127.0.0.1:5000/?data=test_qr_code_data`
* Generate a PDF: `http://127.0.0.1:5000/pdf?data=test_qr_code_data&title=Test%20title&text=Test%20text`
