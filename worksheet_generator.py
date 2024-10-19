from flask import Blueprint, render_template, request, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from models import Worksheet, WorksheetTemplate
from pdf_generator import generate_pdf

worksheet_bp = Blueprint('worksheet', __name__)

@worksheet_bp.route('/dashboard')
@login_required
def dashboard():
    worksheets = Worksheet.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', worksheets=worksheets)

@worksheet_bp.route('/create_worksheet', methods=['GET', 'POST'])
@login_required
def create_worksheet():
    if request.method == 'POST':
        title = request.form.get('title')
        subject = request.form.get('subject')
        grade_level = request.form.get('grade_level')
        topic = request.form.get('topic')
        template_id = request.form.get('template_id')
        content = request.form.get('content')

        new_worksheet = Worksheet(
            title=title,
            subject=subject,
            grade_level=grade_level,
            topic=topic,
            content=content,
            user_id=current_user.id,
            template_id=template_id
        )
        db.session.add(new_worksheet)
        db.session.commit()

        return jsonify({'success': True, 'worksheet_id': new_worksheet.id})

    templates = WorksheetTemplate.query.all()
    return render_template('create_worksheet.html', templates=templates)

@worksheet_bp.route('/preview_worksheet/<int:worksheet_id>')
@login_required
def preview_worksheet(worksheet_id):
    worksheet = Worksheet.query.get_or_404(worksheet_id)
    if worksheet.user_id != current_user.id:
        abort(403)
    return render_template('preview_worksheet.html', worksheet=worksheet)

@worksheet_bp.route('/download_worksheet/<int:worksheet_id>')
@login_required
def download_worksheet(worksheet_id):
    worksheet = Worksheet.query.get_or_404(worksheet_id)
    if worksheet.user_id != current_user.id:
        abort(403)
    
    pdf_file = generate_pdf(worksheet)
    return send_file(pdf_file, as_attachment=True, download_name=f"{worksheet.title}.pdf")

@worksheet_bp.route('/update_worksheet/<int:worksheet_id>', methods=['POST'])
@login_required
def update_worksheet(worksheet_id):
    worksheet = Worksheet.query.get_or_404(worksheet_id)
    if worksheet.user_id != current_user.id:
        abort(403)
    
    worksheet.title = request.form.get('title')
    worksheet.subject = request.form.get('subject')
    worksheet.grade_level = request.form.get('grade_level')
    worksheet.topic = request.form.get('topic')
    worksheet.content = request.form.get('content')
    
    db.session.commit()
    return jsonify({'success': True})

@worksheet_bp.route('/delete_worksheet/<int:worksheet_id>', methods=['POST'])
@login_required
def delete_worksheet(worksheet_id):
    worksheet = Worksheet.query.get_or_404(worksheet_id)
    if worksheet.user_id != current_user.id:
        abort(403)
    
    db.session.delete(worksheet)
    db.session.commit()
    return jsonify({'success': True})
