# 🚀 TDL Expiry Remover - Deployment Guide

This guide covers deployment options for the TDL Expiry Remover application on various platforms.

## 📋 Quick Start

### Option 1: Docker (Recommended)
```bash
# Clone the repository
git clone <your-repo-url>
cd tally-tdl-expiry-remover

# Run deployment script
./deploy.sh
```

### Option 2: Manual Docker
```bash
# Build and run with Docker Compose
docker-compose up --build -d

# Access at http://localhost
```

## 🌐 Deployment Platforms

### 1. Local Development
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Access at http://localhost:5000
```

### 2. Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Git repository

#### Steps
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-tdl-remover-app

# Set stack to container (for Docker)
heroku stack:set container -a your-tdl-remover-app

# Deploy
git push heroku main

# Open application
heroku open -a your-tdl-remover-app
```

#### Environment Variables (if needed)
```bash
heroku config:set FLASK_ENV=production -a your-tdl-remover-app
```

### 3. Railway Deployment

#### Prerequisites
- Railway account
- Git repository connected

#### Steps
1. Visit [Railway](https://railway.app)
2. Connect your GitHub repository
3. Select the repository
4. Railway will automatically detect and deploy using `railway.toml`
5. Your app will be available at the provided Railway URL

### 4. Vercel Deployment

#### Prerequisites
- Vercel account
- Git repository

#### Steps
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow prompts and deploy
```

Or deploy via Vercel Dashboard:
1. Visit [Vercel](https://vercel.com)
2. Import your Git repository
3. Configure using `vercel.json`
4. Deploy

### 5. DigitalOcean App Platform

#### Steps
1. Visit [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Create new app from GitHub repository
3. Configure:
   - **Resource Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `python app.py`
   - **Port**: 5000
4. Deploy

### 6. AWS EC2 Deployment

#### Prerequisites
- AWS account
- EC2 instance (Ubuntu/Amazon Linux)

#### Steps
```bash
# Connect to EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Clone repository
git clone <your-repo-url>
cd tally-tdl-expiry-remover

# Deploy
./deploy.sh

# Configure security group to allow port 80
```

### 7. Google Cloud Run

#### Prerequisites
- Google Cloud account
- gcloud CLI installed

#### Steps
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/tdl-remover

# Deploy to Cloud Run
gcloud run deploy tdl-remover \
  --image gcr.io/YOUR_PROJECT_ID/tdl-remover \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000
```

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=production          # Set to production for live deployment
PORT=5000                     # Port to run the application
MAX_CONTENT_LENGTH=16777216   # Maximum file size (16MB)
```

### File Size Limits
The application supports files up to 16MB by default. To change this:

1. Update `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

2. Update `nginx.conf`:
```nginx
client_max_body_size 32M;
```

## 🔒 Security Considerations

### Production Deployment
1. **Change Secret Key**: Update the Flask secret key in `app.py`
2. **Use HTTPS**: Configure SSL certificates
3. **File Upload Security**: Implement additional file validation
4. **Rate Limiting**: Add rate limiting for uploads
5. **Firewall**: Configure appropriate firewall rules

### Example Security Updates
```python
# In app.py
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate secure key

# Add rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
```

## 📊 Monitoring

### Docker Logs
```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f tdl-remover
```

### Application Health
The application includes basic health endpoints:
- `/` - Main application
- `/cleanup` - Cleanup endpoint

## 🔄 Updates and Maintenance

### Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose up --build -d
```

### Backup
```bash
# Backup uploaded files (if persistent storage needed)
docker cp tdl-expiry-remover:/app/uploads ./uploads-backup
```

## 🆘 Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Kill process using port 5000
sudo lsof -ti:5000 | xargs kill -9
```

2. **Docker Permission Denied**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again
```

3. **File Upload Fails**
- Check file size limits
- Verify file permissions in uploads directory
- Check available disk space

### Log Analysis
```bash
# Check application logs
docker-compose logs tdl-remover

# Check Nginx logs
docker-compose logs nginx

# System logs (on Linux)
tail -f /var/log/syslog
```

## 📞 Support

If you encounter deployment issues:
1. Check the logs using commands above
2. Verify all prerequisites are installed
3. Ensure ports are not blocked by firewall
4. Check available system resources

---

**Note**: Always test deployments in a staging environment before production deployment.