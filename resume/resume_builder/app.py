from flask import Flask, request, send_file, render_template
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import os
import json


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

def check_page_break(p, y_position, threshold):
    """
    Checks if the current y_position is below the threshold for a page break.
    If so, it creates a new page and resets the y_position.
    """
    if y_position < threshold:
        p.showPage()
        p.setFont("Times-Roman", 10)
        return p._pagesize[1] - 50  # Reset y_position to top margin
    return y_position

def draw_wrapped_text(p, text, font_name, font_size, left_margin, right_margin, y_position):
    """
    Draws wrapped text on the PDF canvas.
    """
    p.setFont(font_name, font_size)
    text_object = p.beginText(left_margin, y_position)
    text_object.setFont(font_name, font_size)

    lines = text.split('\n')
    for line in lines:
        wrapped_lines = []
        line = line.strip()
        while len(line) > 0:
            available_width = p._pagesize[0] - left_margin - right_margin
            split_index = len(line)
            while p.stringWidth(line[:split_index], font_name, font_size) > available_width and split_index > 0:
                split_index -= 1
            wrapped_lines.append(line[:split_index])
            line = line[split_index:].lstrip()
        for wrapped_line in wrapped_lines:
            text_object.textLine(wrapped_line)
            y_position -= font_size * 1.5  # Adjust line spacing

    p.drawText(text_object)
    return y_position

@app.route('/generate', methods=['POST'])
def generate():
    # Capture form data
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    country = request.form.get('country', '')
    objective = request.form.get('objective', '')
    education = request.form.get('education', '')
    projects = request.form.get('projects', '')
    work_experience = request.form.get('work_experience', '')
    skills = request.form.get('skills', '')
    achievements = request.form.get('achievements', '')
    languages = request.form.get('languages', '')
    virtual_internships = request.form.get('virtual_internships', '')
    research_papers = request.form.get('research_papers', '')
    certifications = request.form.get('certifications', '')
    extracurricular_activities = request.form.get('extracurricular_activities', '')
    linkedin = request.form.get('linkedin', '')
    github = request.form.get('github', '')

    # Ensure LinkedIn and GitHub links are properly formatted
    if linkedin and not linkedin.startswith(('http://', 'https://')):
        linkedin = 'http://' + linkedin
    if github and not github.startswith(('http://', 'https://')):
        github = 'http://' + github

    

    # Save data to JSON
    save_to_json({
        'name': name,
        'email': email,
        'phone': phone,
        'country': country,
        'objective': objective,
        'education': education,
        'projects': projects,
        'work_experience': work_experience,
        'skills': skills,
        'achievements': achievements,
        'languages': languages,
        'virtual_internships': virtual_internships,
        'research_papers': research_papers,
        'certifications': certifications,
        'extracurricular_activities': extracurricular_activities,
        'linkedin': linkedin,
        'github': github
    })

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Set margins
    top_margin = 50
    left_margin = 50
    right_margin = 50
    bottom_margin = 50

    # Adjust the height and width based on the margins
    y_position = height - top_margin

    # Header Section (centered)
    p.setFont("Times-Roman", 20)
    name_width = p.stringWidth(name, "Times-Roman", 20)
    p.setFillColor(colors.black)
    p.drawString((width - name_width) / 2, y_position, name)
    y_position -= 20

    # Contact Info
    p.setFont("Times-Roman", 10)
    p.setFillColor(colors.black)

    # Prepare contact info strings
    contact_info_parts = []

    # Add email clickable
    if email.strip():
        contact_info_parts.append(f"{email}")

    # Add phone clickable
    if phone.strip():
        contact_info_parts.append(f"| {phone}")

    # Add country
    if country.strip():
        contact_info_parts.append(f"| {country}")

    # Add LinkedIn clickable
    if linkedin.strip():
        contact_info_parts.append(" | LinkedIn")

    # Add GitHub clickable
    if github.strip():
        contact_info_parts.append(" | GitHub")

    # Calculate total width for centering
    total_width = sum(p.stringWidth(part, "Times-Roman", 10) for part in contact_info_parts) + 10 * (len(contact_info_parts) - 1)

    # Calculate starting x position for centering
    x_start = (width - total_width) / 2

    # Draw each part of the contact info
    x_cursor = x_start
    for part in contact_info_parts:
        if part == f"{email}":
            p.setFillColor(colors.blue)  # Set color to blue for email
            p.drawString(x_cursor, y_position, part)
            p.linkURL(f"mailto:{email}", (x_cursor, y_position - 2, x_cursor + p.stringWidth(part, "Times-Roman", 10), y_position + 10), relative=1)
        elif part == f"| {phone}":
            p.setFillColor(colors.black)  # Set color to black for phone
            p.drawString(x_cursor, y_position, part)
            p.linkURL(f"tel:{phone}", (x_cursor, y_position - 2, x_cursor + p.stringWidth(part, "Times-Roman", 10), y_position + 10), relative=1)
        elif part == f"| {country}":
            p.setFillColor(colors.black)  # Set color to black for country
            p.drawString(x_cursor, y_position, part)
        elif part == " | LinkedIn":
            p.setFillColor(colors.blue)  # Set color to blue for LinkedIn
            p.drawString(x_cursor, y_position, part)
            p.linkURL(linkedin, (x_cursor, y_position - 2, x_cursor + p.stringWidth(part, "Times-Roman", 10), y_position + 10), relative=1)
        elif part == " | GitHub":
            p.setFillColor(colors.blue)  # Set color to blue for GitHub
            p.drawString(x_cursor, y_position, part)
            p.linkURL(github, (x_cursor, y_position - 2, x_cursor + p.stringWidth(part, "Times-Roman", 10), y_position + 10), relative=1)
        else:
            p.setFillColor(colors.black)  # Default color to black
            p.drawString(x_cursor, y_position, part)

        x_cursor += p.stringWidth(part, "Times-Roman", 10) + 10  # Add space between parts

    # Move down after contact info
    y_position -= 40

    # Function to check for page break
    def check_page_break(p, y_position, min_y):
        if y_position < min_y:
            p.showPage()
            p.setFont("Times-Roman", 10)
            return height - top_margin
        return y_position

    # Set minimum y_position threshold
    min_y_position = bottom_margin + 50

    # Objective Section
    if objective.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Objective")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, objective, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Education Section
    if education.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Education")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, education, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Projects Section
    if projects.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Projects")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, projects, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Work Experience Section
    if work_experience.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Work Experience")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, work_experience, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Skills Section
    if skills.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Skills")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, skills, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Achievements Section
    if achievements.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Achievements")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, achievements, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Languages Section
    if languages.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Languages")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, languages, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Virtual Internships Section
    if virtual_internships.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Virtual Internships")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, virtual_internships, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Research Papers Section
    if research_papers.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Research Papers")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, research_papers, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Certifications Section
    if certifications.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Certifications")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, certifications, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Extracurricular Activities Section
    if extracurricular_activities.strip():
        y_position = check_page_break(p, y_position, min_y_position)
        p.setFont("Times-Bold", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin, y_position, "Extracurricular Activities")
        y_position -= 5
        p.setFillColor(colors.black)
        p.line(left_margin, y_position, width - right_margin, y_position)
        y_position -= 15
        y_position = draw_wrapped_text(p, extracurricular_activities, "Times-Roman", 10, left_margin, right_margin, y_position)

    # Finalize the PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='resume.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)