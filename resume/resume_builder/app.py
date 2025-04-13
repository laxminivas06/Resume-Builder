from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from reportlab.lib import colors

app = Flask(__name__)

# Register fonts
pdfmetrics.registerFont(TTFont('Times-Roman', 'Times New Roman.ttf'))  # Regular Times New Roman
pdfmetrics.registerFont(TTFont('Times-Roman-Bold', 'Times New Roman Bold.ttf'))  # Bold Times New Roman

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Capture form data
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    country = request.form.get('country', '')
    education = request.form.get('education', '')
    projects = request.form.get('projects', '')
    work_experience = request.form.get('work_experience', '')
    skills = request.form.get('skills', '')
    achievements = request.form.get('achievements', '')

    # Create PDF with proper margins
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4  # Get the width and height of the A4 page
    margin = 50  # Define your margin
    y_position = height - margin  # Start from the top of the page

    # Function to wrap and draw text on the PDF canvas
    def draw_wrapped_text(text, font_name, line_spacing=1.5, font_size=12):
        nonlocal y_position  # Use nonlocal to modify the outer y_position variable
        p.setFont(font_name, font_size)
        text_object = p.beginText(margin, y_position)
        text_object.setFont(font_name, font_size)

        lines = text.split('\n')
        for line in lines:
            wrapped_lines = []
            line = line.strip()
            # Wrap the text to fit within the available width
            while len(line) > 0:
                # Check if the line is too long
                available_width = width - 2 * margin
                split_index = len(line)
                while p.stringWidth(line[:split_index], font_name, font_size) > available_width and split_index > 0:
                    split_index -= 1
                wrapped_lines.append(line[:split_index])
                line = line[split_index:].lstrip()
            # If the line is too long, split it into multiple lines
            
            while line:
                available_width = width - 2 * margin
                split_index = len(line)
                while p.stringWidth(line[:split_index], font_name, font_size) > available_width and split_index > 0:
                    split_index -= 1
                wrapped_lines.append(line[:split_index])
                line = line[split_index:].lstrip()
            for wrapped_line in wrapped_lines:
                text_object.textLine(wrapped_line)
                y_position -= font_size * line_spacing  # Update y_position for the next line

        p.drawText(text_object)  # Draw the text object on the canvas

    # Define the color for headings
    heading_color = colors.HexColor('#004aad')

    # Header Section (centered)
    p.setFont("Times-Roman", 20)  # Use Times New Roman for the name
    name_width = p.stringWidth(name, "Times-Roman", 20)
    p.drawString((width - name_width) / 2, y_position, name)
    y_position -= 20

    # Updated contact info
    contact_info = f" {email} |  {phone} |  {country}"
    p.setFont("Times-Roman", 10)  # Use Times New Roman for contact info
    contact_width = p.stringWidth(contact_info, "Times-Roman", 10)
    p.drawString((width - contact_width) / 2, y_position, contact_info)
    y_position -= 40

    # EDUCATION Section
    p.setFillColor(heading_color)  # Set color for education heading
    p.setFont("Times-Roman-Bold", 14)  # Use Times New Roman Bold for section titles
    p.drawString(margin, y_position, "EDUCATION")
    y_position -= 5
    p.line(margin, y_position, width - margin, y_position)  # Draw horizontal line
    y_position -= 20
    p.setFillColor(colors.black)  # Set paragraph text color to black
    draw_wrapped_text(education, "Times-Roman", line_spacing=1.50)

    # PROJECTS Section
    p.setFillColor(heading_color)  # Set color for projects heading
    p.setFont("Times-Roman-Bold", 14)
    p.drawString(margin, y_position, "PROJECTS")
    y_position -= 5
    p.line(margin, y_position, width - margin, y_position)  # Draw horizontal line
    y_position -= 20
    p.setFillColor(colors.black)  # Set paragraph text color to black
    draw_wrapped_text(projects, "Times-Roman", line_spacing=1.50)

    # Work Experience Section
    p.setFillColor(heading_color)  # Set color for work experience heading
    p.setFont("Times-Roman-Bold", 14)
    p.drawString(margin, y_position, "WORK EXPERIENCE")
    y_position -= 5
    p.line(margin, y_position, width - margin, y_position)  # Draw horizontal line
    y_position -= 20
    p.setFillColor(colors.black)  # Set paragraph text color to black
    draw_wrapped_text(work_experience, "Times-Roman", line_spacing=1.50)

    # SKILLS Section
    p.setFillColor(heading_color)  # Set color for skills heading
    p.setFont("Times-Roman-Bold", 14)
    p.drawString(margin, y_position, "SKILLS")
    y_position -= 5
    p.line(margin, y_position, width - margin, y_position)  # Draw horizontal line
    y_position -= 20
    p.setFillColor(colors.black)  # Set paragraph text color to black
    draw_wrapped_text(skills, "Times-Roman", line_spacing=1.50)

    # ACHIEVEMENTS Section
    p.setFillColor(heading_color)  # Set color for achievements heading
    p.setFont("Times-Roman-Bold", 14)
    p.drawString(margin, y_position, "ACHIEVEMENTS")
    y_position -= 5
    p.line(margin, y_position, width - margin, y_position)  # Draw horizontal line
    y_position -= 20
    p.setFillColor(colors.black)  # Set paragraph text color to black
    draw_wrapped_text(achievements, "Times-Roman", line_spacing=1.50)

    # Finalize the PDF
    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='resume.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)