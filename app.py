from flask import Flask, request, render_template, send_file, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import re
import tempfile
import shutil
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'tdl', 'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_tdl_expiry(file_content):
    """
    Remove expiry date patterns from TDL file content
    """
    # Common TDL expiry patterns
    expiry_patterns = [
        # Date patterns like DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY
        r'(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{4})',
        # Expiry related keywords
        r'(?i)expiry\s*[:=]\s*["\']?([^"\';\n\r]*)["\']?',
        r'(?i)expire\s*[:=]\s*["\']?([^"\';\n\r]*)["\']?',
        r'(?i)valid\s*till\s*[:=]\s*["\']?([^"\';\n\r]*)["\']?',
        r'(?i)valid\s*upto\s*[:=]\s*["\']?([^"\';\n\r]*)["\']?',
        r'(?i)trial\s*period\s*[:=]\s*["\']?([^"\';\n\r]*)["\']?',
        r'(?i)license\s*expiry\s*[:=]\s*["\']?([^"\';\n\r]*)["\']?',
        # Common TDL validation functions
        r'(?i)##\s*sysinfo\s*:\s*expiry\s*date[^\n\r]*',
        r'(?i)##\s*sysinfo\s*:\s*trial[^\n\r]*',
        # Version and date validation
        r'(?i)version\s*validation[^\n\r]*',
        r'(?i)date\s*validation[^\n\r]*',
        # License check functions
        r'(?i)license\s*check[^\n\r]*',
        r'(?i)validity\s*check[^\n\r]*',
        # TDL specific expiry functions
        r'\$\$IsSysInfoExpiry[^\n\r]*',
        r'\$\$IsTrialExpired[^\n\r]*',
        r'\$\$CheckExpiry[^\n\r]*',
        r'\$\$ValidityCheck[^\n\r]*',
        # Remove specific date comparisons
        r'(?i)if\s*:\s*\$\$Date[^\n\r]*>=[^\n\r]*',
        r'(?i)if\s*:\s*\$\$Date[^\n\r]*<=[^\n\r]*',
        r'(?i)if\s*:\s*\$\$Date[^\n\r]*=[^\n\r]*',
    ]
    
    modified_content = file_content
    
    # Remove expiry patterns
    for pattern in expiry_patterns:
        modified_content = re.sub(pattern, '', modified_content)
    
    # Remove empty lines created by removals
    modified_content = re.sub(r'\n\s*\n\s*\n', '\n\n', modified_content)
    
    # Remove comments that might contain expiry info
    modified_content = re.sub(r';;.*expiry.*\n', '\n', modified_content, flags=re.IGNORECASE)
    modified_content = re.sub(r';;.*expire.*\n', '\n', modified_content, flags=re.IGNORECASE)
    modified_content = re.sub(r';;.*trial.*\n', '\n', modified_content, flags=re.IGNORECASE)
    
    return modified_content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Read file content
            file_content = file.read().decode('utf-8', errors='ignore')
            
            # Remove expiry date patterns
            modified_content = remove_tdl_expiry(file_content)
            
            # Save modified file
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            modified_filename = f"{name}_no_expiry{ext}"
            
            modified_file_path = os.path.join(app.config['UPLOAD_FOLDER'], modified_filename)
            
            with open(modified_file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            return jsonify({
                'success': True,
                'message': 'TDL expiry removed successfully!',
                'download_url': url_for('download_file', filename=modified_filename),
                'filename': modified_filename
            })
            
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type. Please upload TDL files only.'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/cleanup')
def cleanup_files():
    """Clean up old files"""
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return jsonify({'success': True, 'message': 'Files cleaned up successfully'})
    except Exception as e:
        return jsonify({'error': f'Cleanup error: {str(e)}'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)