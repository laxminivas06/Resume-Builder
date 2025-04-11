from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Capture all the form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    country = request.form.get('country')
    linkedin = request.form.get('linkedin')
    github = request.form.get('github')
    education = request.form.get('education')
    projects = request.form.get('projects')
    work_experience = request.form.get('work_experience')
    skills = request.form.get('skills')
    achievements = request.form.get('achievements')

    # Create PDF with proper margins
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Set margins (1 inch all around)
    margin = inch
    width, height = A4
    content_width = width - 2 * margin
    
    # Starting position (top of page minus top margin)
    y_position = height - margin
    
    # Helper function to draw wrapped text
    def draw_wrapped_text(text, style="Helvetica", size=12, bold=False, indent=0):
        nonlocal y_position
        if bold:
            p.setFont(f"{style}-Bold", size)
        else:
            p.setFont(style, size)
            
        text_lines = text.splitlines()
        for line in text_lines:
            words = line.split()
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                if p.stringWidth(test_line, style, size) < content_width - indent:
                    current_line.append(word)
                else:
                    if current_line:
                        p.drawString(margin + indent, y_position, ' '.join(current_line))
                        y_position -= size
                    current_line = [word]
            if current_line:
                p.drawString(margin + indent, y_position, ' '.join(current_line))
                y_position -= size
        y_position -= size/2  # Add small space after paragraph

    # Header Section (centered)
    p.setFont("Helvetica-Bold", 20)
    name_width = p.stringWidth(name, "Helvetica-Bold", 20)
    p.drawString((width - name_width)/2, y_position, name)
    y_position -= 30
    
    contact_info = f"✉ {email} | 📞 {phone} | 🇮🇳 {country} | LinkedIn: {linkedin} | GitHub: {github}"
    p.setFont("Helvetica", 10)
    contact_width = p.stringWidth(contact_info, "Helvetica", 10)
    p.drawString((width - contact_width)/2, y_position, contact_info)
    y_position -= 40

    # Education Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margin, y_position, "EDUCATION")
    y_position -= 20
    draw_wrapped_text(education)
    
    
    # Projects Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margin, y_position, "PROJECTS")
    y_position -= 20
    draw_wrapped_text(projects, indent=10)

    # Work Experience Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margin, y_position, "WORK EXPERIENCE")
    y_position -= 20
    draw_wrapped_text(work_experience, indent=10)

    # Skills Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margin, y_position, "SKILLS")
    y_position -= 20
    draw_wrapped_text(skills, indent=10)

    # Achievements Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margin, y_position, "ACHIEVEMENTS")
    y_position -= 20
    draw_wrapped_text(achievements, indent=10)

    # Finalize PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='resume.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)