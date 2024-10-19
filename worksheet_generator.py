import logging
from flask import Blueprint, render_template, request, jsonify, send_file, abort, redirect, url_for
from flask_login import login_required, current_user
from app import db
from models import Worksheet, WorksheetTemplate, User
from pdf_generator import generate_pdf

worksheet_bp = Blueprint('worksheet', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@worksheet_bp.route('/dashboard')
@login_required
def dashboard():
    own_worksheets = Worksheet.query.filter_by(user_id=current_user.id).all()
    shared_worksheets = Worksheet.query.filter(Worksheet.is_shared == True, Worksheet.shared_with.contains(str(current_user.id))).all()
    return render_template('dashboard.html', own_worksheets=own_worksheets, shared_worksheets=shared_worksheets)

@worksheet_bp.route('/create_worksheet', methods=['GET', 'POST'])
@login_required
def create_worksheet():
    if request.method == 'POST':
        try:
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

            logger.info(f"Worksheet created: {new_worksheet.id} by user {current_user.id}")
            return jsonify({'success': True, 'worksheet_id': new_worksheet.id})
        except Exception as e:
            logger.error(f"Error creating worksheet: {str(e)}")
            db.session.rollback()
            return jsonify({'success': False, 'error': 'An error occurred while creating the worksheet'}), 500

    templates = WorksheetTemplate.query.all()
    return render_template('create_worksheet.html', templates=templates)

@worksheet_bp.route('/get_template/<int:template_id>')
@login_required
def get_template(template_id):
    template = WorksheetTemplate.query.get_or_404(template_id)
    return jsonify({'success': True, 'content': template.content})

@worksheet_bp.route('/preview_worksheet/<int:worksheet_id>')
@login_required
def preview_worksheet(worksheet_id):
    worksheet = Worksheet.query.get_or_404(worksheet_id)
    if worksheet.user_id != current_user.id and not (worksheet.is_shared and str(current_user.id) in worksheet.shared_with.split(',')):
        abort(403)
    return render_template('preview_worksheet.html', worksheet=worksheet)

@worksheet_bp.route('/download_worksheet/<int:worksheet_id>')
@login_required
def download_worksheet(worksheet_id):
    worksheet = Worksheet.query.get_or_404(worksheet_id)
    if worksheet.user_id != current_user.id and not (worksheet.is_shared and str(current_user.id) in worksheet.shared_with.split(',')):
        abort(403)
    
    pdf_file = generate_pdf(worksheet)
    return send_file(pdf_file, as_attachment=True, download_name=f"{worksheet.title}.pdf")

@worksheet_bp.route('/update_worksheet/<int:worksheet_id>', methods=['POST'])
@login_required
def update_worksheet(worksheet_id):
    worksheet = Worksheet.query.get_or_404(worksheet_id)
    if worksheet.user_id != current_user.id:
        abort(403)
    
    try:
        worksheet.title = request.form.get('title')
        worksheet.subject = request.form.get('subject')
        worksheet.grade_level = request.form.get('grade_level')
        worksheet.topic = request.form.get('topic')
        worksheet.content = request.form.get('content')
        
        db.session.commit()
        logger.info(f"Worksheet updated: {worksheet_id} by user {current_user.id}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error updating worksheet: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'An error occurred while updating the worksheet'}), 500

@worksheet_bp.route('/delete_worksheet/<int:worksheet_id>', methods=['POST'])
@login_required
def delete_worksheet(worksheet_id):
    worksheet = Worksheet.query.get_or_404(worksheet_id)
    if worksheet.user_id != current_user.id:
        abort(403)
    
    try:
        db.session.delete(worksheet)
        db.session.commit()
        logger.info(f"Worksheet deleted: {worksheet_id} by user {current_user.id}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error deleting worksheet: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'An error occurred while deleting the worksheet'}), 500

@worksheet_bp.route('/share_worksheet/<int:worksheet_id>', methods=['GET', 'POST'])
@login_required
def share_worksheet(worksheet_id):
    worksheet = Worksheet.query.get_or_404(worksheet_id)
    if worksheet.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        shared_usernames = request.form.get('shared_usernames', '').split(',')
        shared_users = User.query.filter(User.username.in_(shared_usernames)).all()
        
        if not shared_users:
            return jsonify({'success': False, 'error': 'No valid users found to share with'}), 400

        worksheet.is_shared = True
        worksheet.shared_with = ','.join([str(user.id) for user in shared_users])
        db.session.commit()
        logger.info(f"Worksheet shared: {worksheet_id} by user {current_user.id} with users {worksheet.shared_with}")
        return jsonify({'success': True})

    return render_template('share_worksheet.html', worksheet=worksheet)
