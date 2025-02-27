# 🔗 LinkShrink

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)


**LinkShrink** is a sleek, minimalist URL shortener built with Flask. It transforms lengthy URLs into concise, shareable links—no account required. A perfect solution for cleaner links in emails, messages, or social media posts.

## ✨ Features

- **No Registration Required** - Create shortened links instantly without signing up
- **Visit Tracking** - Monitor how many times your shortened link has been clicked
- **Link Expiration** - All links automatically expire after a configurable period (default: 30 days)
- **IP-based Link Management** - View all your created links based on your IP address/cookie
- **Analytics** - Basic analytics showing visit counts for link creators
- **Responsive UI** - Clean, modern interface that works on all devices
- **One-Click Copy** - Easily copy shortened URLs to clipboard
- **Time-Remaining Display** - See how much time is left before your link expires
- **Docker Ready** - Deploy easily with included Docker configuration
- **Multiple Deployment Options** - Run with Waitress, Gunicorn, or Docker

## 📋 Table of Contents

- [🔗 LinkShrink](#-linkshrink)
  - [✨ Features](#-features)
  - [📋 Table of Contents](#-table-of-contents)
  - [🚀 Installation](#-installation)
    - [Standard Installation](#standard-installation)
    - [Docker Installation](#docker-installation)
  - [⚙️ Configuration](#️-configuration)
  - [🌐 Deployment Options](#-deployment-options)
    - [Development Server](#development-server)
    - [Production Server - Windows (Waitress)](#production-server---windows-waitress)
    - [Production Server - Linux (Gunicorn)](#production-server---linux-gunicorn)
    - [Docker Deployment](#docker-deployment)
  - [🏗️ Architecture](#️-architecture)
  - [🔒 Security Considerations](#-security-considerations)
  - [🚀 Performance \& Scaling](#-performance--scaling)
  - [👥 Contributing](#-contributing)
  - [📝 License](#-license)

## 🚀 Installation

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/LinkShrink.git
cd LinkShrink

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env file with your settings

# Run the application (development mode)
python run.py
```

### Docker Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/LinkShrink.git
cd LinkShrink

# Configure environment
cp .env.example .env
# Edit .env file with your settings

# Build and run with Docker Compose
docker-compose up -d
```

## ⚙️ Configuration

LinkShrink can be configured using environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Application environment (development/production) | `production` |
| `APP_SECRET_KEY` | Secret key for sessions and CSRF protection | `default-secret-key` |
| `DATABASE_URI` | Database connection string | `sqlite:///linkshrink.db` |
| `MAX_URL_LENGTH` | Maximum length for original URLs | `2000` |
| `DEFAULT_EXPIRATION_DAYS` | Days before URLs expire | `30` |
| `PROXY_COUNT` | Number of proxies in front of the application | `0` |
| `SSL_REDIRECT` | Whether to redirect HTTP to HTTPS | `False` |
| `EXPIRE_LINKS_CHECK_TIME_SEC` | How often to check for expired links (seconds) | `60` |

## 🌐 Deployment Options

### Development Server

For development purposes only:

```bash
python run.py
```

### Production Server - Windows (Waitress)

[Waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/) is a production-quality pure-Python WSGI server for Windows:

```bash
# Install Waitress
pip install waitress

# Run with Waitress
python -m waitress --port=8000 run:app
```

### Production Server - Linux (Gunicorn)

[Gunicorn](https://gunicorn.org/) is a Python WSGI HTTP Server for UNIX:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 run:app
```

For production deployment, consider adding a process manager like Supervisor:

```bash
# Example supervisor configuration (/etc/supervisor/conf.d/linkshrink.conf)
[program:linkshrink]
command=/path/to/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 run:app
directory=/path/to/LinkShrink
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/linkshrink/error.log
stdout_logfile=/var/log/linkshrink/access.log
```

### Docker Deployment

For easy deployment with Docker:

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f
```

For production Docker deployment:

```bash
# Start with production settings
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🏗️ Architecture

LinkShrink uses a simple but effective architecture:

- **Flask**: Web framework handling routes and requests
- **SQLite**: Simple database for storing URL information
- **Expiration System**: Background process monitoring link expiration
- **Cookie-based Auth**: Simple identifier to track link creators
- **Responsive Frontend**: Modern UI using TailwindCSS

## 🔒 Security Considerations

- The application uses cookies to identify users (no login required)
- CSRF protection is implemented for form submissions
- No sensitive data is stored about users or links
- Consider using HTTPS in production environments
- The Docker setup includes security best practices

## 🚀 Performance & Scaling

LinkShrink is designed for small to medium-scale use. For high-traffic scenarios, consider:

- **Database**: Replace SQLite with PostgreSQL or MongoDB
- **Caching**: Implement Redis for caching frequently accessed URLs
- **Load Balancing**: Deploy multiple instances behind a load balancer
- **CDN**: Use a CDN for static assets
- **Rate Limiting**: Implement API rate limiting to prevent abuse
- **Optimization**: The current code prioritizes simplicity over optimization

## 👥 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

**What is [MIT](https://choosealicense.com/licenses/mit/) License?** The MIT license is a permissive free software license originating at the Massachusetts Institute of Technology (MIT). As a permissive license, it puts only very limited restriction on reuse and has, therefore, high license compatibility. The MIT license permits reuse within proprietary software provided all copies of the licensed software include a copy of the MIT License terms and the copyright notice.

---

<p align="center">Made with ❤️ by Olger Chotza, Thessaloníki, Greece.</p>