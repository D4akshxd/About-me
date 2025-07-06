let selectedFile = null;
let downloadUrl = null;

// Initialize file input handler
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const uploadContainer = document.getElementById('uploadContainer');
    
    // File input change handler
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    // Drag and drop handlers
    uploadContainer.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadContainer.style.borderColor = '#667eea';
        uploadContainer.style.background = '#f8f9ff';
    });
    
    uploadContainer.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadContainer.style.borderColor = '#ddd';
        uploadContainer.style.background = '';
    });
    
    uploadContainer.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadContainer.style.borderColor = '#ddd';
        uploadContainer.style.background = '';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
});

function handleFileSelect(file) {
    // Validate file type
    const allowedTypes = ['tdl', 'txt'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
        showError('Please select a valid TDL file (.tdl or .txt)');
        return;
    }
    
    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size too large. Maximum size is 16MB');
        return;
    }
    
    selectedFile = file;
    
    // Update UI
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = `Size: ${formatFileSize(file.size)}`;
    
    // Show process section and hide upload section
    document.querySelector('.upload-section').style.display = 'none';
    document.getElementById('processSection').style.display = 'block';
}

function removeFile() {
    selectedFile = null;
    downloadUrl = null;
    
    // Reset file input
    document.getElementById('fileInput').value = '';
    
    // Show upload section and hide others
    document.querySelector('.upload-section').style.display = 'block';
    document.getElementById('processSection').style.display = 'none';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
}

function processFile() {
    if (!selectedFile) {
        showError('No file selected');
        return;
    }
    
    // Show loading section
    document.getElementById('processSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'block';
    
    // Create form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    // Upload and process file
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingSection').style.display = 'none';
        
        if (data.success) {
            downloadUrl = data.download_url;
            showResult(data.message, data.filename);
        } else {
            showError(data.error || 'Processing failed');
            document.getElementById('processSection').style.display = 'block';
        }
    })
    .catch(error => {
        document.getElementById('loadingSection').style.display = 'none';
        document.getElementById('processSection').style.display = 'block';
        showError('Network error: ' + error.message);
    });
}

function showResult(message, filename) {
    // Update download button
    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.onclick = function() {
        if (downloadUrl) {
            window.location.href = downloadUrl;
        }
    };
    
    // Show result section
    document.getElementById('resultSection').style.display = 'block';
}

function resetForm() {
    selectedFile = null;
    downloadUrl = null;
    
    // Reset file input
    document.getElementById('fileInput').value = '';
    
    // Show upload section and hide others
    document.querySelector('.upload-section').style.display = 'block';
    document.getElementById('processSection').style.display = 'none';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
    
    // Clear any error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
}

function showError(message) {
    // Remove existing error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Create new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
    
    // Insert after main content
    const mainContent = document.querySelector('.main-content');
    mainContent.appendChild(errorDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Additional utility functions for future enhancements
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
    
    const mainContent = document.querySelector('.main-content');
    mainContent.appendChild(successDiv);
    
    setTimeout(() => {
        if (successDiv.parentNode) {
            successDiv.remove();
        }
    }, 3000);
}

function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename || 'processed_file.tdl';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}