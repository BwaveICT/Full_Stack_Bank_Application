from app import app
from flask import render_template, send_file
from datetime import datetime
import os, tempfile
import pdfkit


@app.route('/download_reciept/<filename>')
def download_reciept(filename):
    #provide the reciept file for downloading
    return send_file(filename, as_attachment=True)


@app.route('/success/<filename>')
def payment(filename):
    return render_template('user/payment.html', filename=filename)

@app.route('/success/<filename>/download')
def downlaod_success_reciept(filename):
    #provide the reciept for downloading
    return send_file(filename, as_attachment=True)


def generate_receipt(reciept_data):
    # define a part to the html template file
    html_template_path = "app/templates/user/receipt_template.html"

    # Read HTML content from the seprate file
    with open(html_template_path, "r") as file:
        receipt_content = file.read()

    # Format the HTMML content with reciept data
    receipt_content =  receipt_content.format(**reciept_data)

    # Generate a unique filename for the reciept using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'reciept_{timestamp}.pdf'

    #create a tempory directory
    temp_dir = tempfile.mkdtemp()

    # save the html content to a tempory file
    temp_html_path = os.path.join(temp_dir, "temp_receipt.html")
    with open(temp_html_path, "w") as temp_file:
        temp_file.write(receipt_content)

    pdf_path = os.path.join(temp_dir, filename)
    pdfkit.from_file(temp_html_path, pdf_path)

    #clean the temp html file
    os.remove(temp_html_path)

    return pdf_path