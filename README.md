# Tally Prime TDL Expiry Remover

A web application that removes expiry dates from Tally Prime TDL (Tally Definition Language) files, making them work permanently without time restrictions.

## Features

- ✅ **Safe Processing**: Your original file remains unchanged
- ⏰ **Permanent Solution**: Remove all expiry restrictions from TDL files
- ⚡ **Fast Processing**: Quick and efficient with intelligent pattern recognition
- 🔒 **Secure**: Files are processed locally and automatically cleaned up
- 📱 **Modern UI**: Beautiful, responsive design that works on all devices
- 🎯 **Easy to Use**: Simple drag-and-drop interface

## How It Works

1. Upload your TDL file (.tdl or .txt format)
2. Click "Remove TDL Expiry" to process the file
3. Download the fresh TDL file without expiry restrictions
4. Use the processed TDL file in Tally Prime

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to `http://localhost:5000`

## Usage

1. **Upload File**: Click "Browse Files" or drag & drop your TDL file
2. **Process**: Click "Remove TDL Expiry" button
3. **Download**: Click "Download Fresh TDL" to get the processed file
4. **Install**: Copy the processed TDL file to your Tally directory

## Supported File Types

- `.tdl` - Tally Definition Language files
- `.txt` - Text files containing TDL code

## Technical Details

The application removes various expiry patterns including:
- Date patterns (DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY)
- Expiry keywords and validations
- Trial period restrictions
- License expiry checks
- TDL-specific expiry functions
- Date comparison operations

## File Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Main web interface
├── static/
│   ├── css/
│   │   └── style.css  # Styling
│   └── js/
│       └── script.js  # Frontend functionality
└── uploads/           # Temporary file storage
```

## API Endpoints

- `GET /` - Main interface
- `POST /upload` - Process TDL file
- `GET /download/<filename>` - Download processed file
- `GET /cleanup` - Clean temporary files

## Security Features

- File type validation
- File size limits (16MB max)
- Secure filename handling
- Automatic cleanup of processed files
- Input sanitization

## Configuration

You can modify these settings in `app.py`:
- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)
- `UPLOAD_FOLDER`: Directory for temporary files
- `ALLOWED_EXTENSIONS`: Supported file types

## Browser Support

- Chrome/Chromium 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Disclaimer

This tool is for educational purposes. Please ensure you have the right to modify TDL files and comply with Tally's terms of service.

## License

This project is open source. Use responsibly and at your own discretion.

## Support

If you encounter any issues or have questions, please create an issue in the repository.

---

**Note**: Always backup your original TDL files before processing. This tool creates new files without modifying originals.
