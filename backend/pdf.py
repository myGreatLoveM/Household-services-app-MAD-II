import pdfkit

# Path to the wkhtmltopdf executable (only required for Windows)
path_to_wkhtmltopdf = '/path/to/wkhtmltopdf'

# HTML content or path to the HTML file
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Example</title>
</head>
<body>
    <h1>Booking Information</h1>
    <p>This PDF contains booking details.</p>
</body>
</html>
"""

# Save HTML as PDF
options = {
    'page-size': 'A4',
    'encoding': 'UTF-8',
    'no-outline': None
}

# Use pdfkit to create a PDF from the HTML string
pdfkit.from_string(html_content, 'output.pdf', options=options)
