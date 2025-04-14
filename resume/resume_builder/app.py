from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
import json
import os

app = Flask(__name__)

# Path to the JSON file
json_file_path = 'resumes.json'

def save_to_json(data):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = []

    existing_data.append(data)

    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    country = request.form.get('country', '')
    education = request.form.get('education', '')
    projects = request.form.get('projects', '')
    work_experience = request.form.get('work_experience', '')
    skills = request.form.get('skills', '')
    achievements = request.form.get('achievements', '')

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 50
    y_position = height - margin

    def draw_wrapped_text(text, font_name, line_spacing=1.5, font_size=12):
        nonlocal y_position
        p.setFont(font_name, font_size)
        text_object = p.beginText(margin, y_position)
        text_object.setFont(font_name, font_size)

        lines = text.split('\n')
        for line in lines:
            wrapped_lines = []
            line = line.strip()
            while len(line) > 0:
                available_width = width - 2 * margin
                split_index = len(line)
                while p.stringWidth(line[:split_index], font_name, font_size) > available_width and split_index > 0:
                    split_index -= 1
                wrapped_lines.append(line[:split_index])
                line = line[split_index:].lstrip()
            while line:
                available_width = width - 2 * margin
                split_index = len(line)
                while p.stringWidth(line[:split_index], font_name, font_size) > available_width and split_index > 0:
                    split_index -= 1
                wrapped_lines.append(line[:split_index])
                line = line[split_index:].lstrip()
            for wrapped_line in wrapped_lines:
                text_object.textLine(wrapped_line)
                y_position -= font_size * line_spacing

        p.drawText(text_object)

    heading_color = colors.HexColor('#004aad')

    # Use predefined font names
    p.setFont("Times-Roman", 20)  # Use Times New Roman for the name
    name_width = p.stringWidth(name, "Times-Roman", 20)
    p.drawString((width - name_width) / 2, y_position, name)
    y_position -= 20

    contact_info = f" {email} |  {phone} |  {country}"
    p.setFont("Times-Roman", 10)  # Use Times New Roman for contact info
    contact_width = p.stringWidth(contact_info, "Times-Roman", 10)
    p.drawString((width - contact_width) / 2, y_position, contact_info)
    y_position -= 40

    # EDUCATION Section
    p.setFillColor(heading_color)
    p.setFont("Times-Bold", 14)  # Use Times New Roman Bold for section titles
    p.drawString(margin, y_position, "EDUCATION")
    y_position -= 5
    p.line(margin, y_position, width - margin, y_position)
    y_position -= 20
    p.setFillColor(colors.black)
    draw_wrapped_text(education, "Times-Roman", line_spacing=1.50)

    # PROJECTS Section
    p.setFillColor(heading_color)
    p.setFont("Times-Bold", 14)
    p.drawString(margin, y_position, "PROJECTS")
    y_position -= 5
    p.line(margin, y_position, width - margin , y_position)
    y_position -= 20
    p.setFillColor(colors.black)
    draw_wrapped_text(projects, "Times-Roman", line_spacing=1.50)

    # WORK EXPERIENCE Section
    p.setFillColor(heading_color)
    p.setFont("Times-Bold", 14)
    p.drawString(margin, y_position, "WORK EXPERIENCE")
    y_position -= 5
    p.line(margin, y_position, width - margin, y_position)
    y_position -= 20
    p.setFillColor(colors.black)
    draw_wrapped_text(work_experience, "Times-Roman", line_spacing=1.50)

    # SKILLS Section
    p.setFillColor(heading_color)
    p.setFont("Times-Bold", 14)
    p.drawString(margin, y_position, "SKILLS")
    y_position -= 5
    p.line(margin, y_position, width - margin, y_position)
    y_position -= 20
    p.setFillColor(colors.black)
    draw_wrapped_text(skills, "Times-Roman", line_spacing=1.50)

    # ACHIEVEMENTS Section
    p.setFillColor(heading_color)
    p.setFont("Times-Bold", 14)
    p.drawString(margin, y_position, "ACHIEVEMENTS")
    y_position -= 5
    p.line(margin, y_position, width - margin, y_position)
    y_position -= 20
    p.setFillColor(colors.black)
    draw_wrapped_text(achievements, "Times-Roman", line_spacing=1.50)

    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='resume.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)