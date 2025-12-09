# One Cup Initiative Website

A comprehensive Django web application for the One Cup Initiative - a sustainable movement empowering farmers, training youth, and restoring our planet through innovative coffee and tree planting programs.

## 📚 Documentation

- **[ADMIN_DOCUMENTATION.md](ADMIN_DOCUMENTATION.md)** - Comprehensive admin guide including media files management

## 🌟 Features

### Core Functionality
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **User Authentication**: Role-based access control (Admin, Partner, Donor, Volunteer, Visitor, Student)
- **Multilingual Support**: English, French, and Kinyarwanda
- **Impact Tracking**: Real-time statistics for trees planted, youth trained, and environmental impact

### Programs
- **Coffee Farmer Support**: Seedling distribution, training, and market access
- **Youth Barista Academy**: Comprehensive training programs with scholarship opportunities
- **One Cup Campaign**: Tree planting tracking with digital certificates

### Additional Features
- **E-commerce Integration**: Shop for reusable cups, coffee, and tree sponsorships
- **Event Management**: Registration and calendar integration
- **Media Gallery**: Blog, photo galleries, and video content
- **Contact System**: Inquiry management and newsletter integration
- **API Ready**: Django REST Framework for mobile app integration

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or extract the project**
   ```bash
   cd onecup_one_tree_website
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file and add your configuration
   # At minimum, set SECRET_KEY and email settings
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the website**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## 📁 Project Structure

```
onecup_one_tree_website/
├── apps/                          # Django applications
│   ├── accounts/                  # User management and authentication
│   ├── api/                       # REST API endpoints
│   ├── contact/                   # Contact forms and inquiries
│   ├── core/                      # Core functionality and homepage
│   ├── events/                    # Event management
│   ├── media/                     # Blog, gallery, and media content
│   ├── programs/                  # Farmer support, barista academy, tree campaign
│   └── shop/                      # E-commerce functionality
├── templates/                     # HTML templates
│   ├── base.html                  # Base template with navigation
│   └── core/                      # Core app templates
├── static/                        # Static files (CSS, JS, images)
├── media/                         # User-uploaded files
├── onecup_one_tree_website/       # Project settings
│   ├── settings.py                # Django configuration
│   ├── urls.py                    # URL routing
│   └── wsgi.py                    # WSGI configuration
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🛠 Development

### Adding New Features

1. **Create new Django apps** (if needed)
   ```bash
   python manage.py startapp new_app_name
   ```

2. **Add to INSTALLED_APPS** in `settings.py`

3. **Create models** in `models.py`

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create views and templates**

### Customization

#### Styling
- The project uses Bootstrap 5 with custom CSS variables
- All theme colors are defined in `static/css/main.css` using CSS variables:
  ```css
  --color-primary: #fd9d02
  --color-primary-dark: #4b2e1a
  --color-accent: #d2700d
  ```
- Modify these variables to change the site's color scheme
- Social media icon colors are also defined as CSS variables
- No need to change colors throughout templates - just update CSS variables

#### Content
- All site content (name, description, contact info) is managed through environment variables
- Update `.env` file to change site information
- Social media links are also configured in `.env`
- No hardcoded values in templates - everything uses Django context

## 🔧 Configuration

### Environment Variables

The project uses environment variables for configuration to keep sensitive data secure and make deployment easier. All configuration is done through environment variables defined in a `.env` file.

**Setup:**

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your values:
   ```env
   # Django Core Settings
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

   # Email Configuration
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   CONTACT_NOTIFICATION_EMAIL=info@onecupinitiative.org

   # Site Information (optional - has defaults)
   SITE_NAME=One Cup Initiative
   CONTACT_PHONE=+250 788 354 403
   CONTACT_ADDRESS=16 KG 599 Street, Kigali

   # Social Media Links (optional - has defaults)
   SOCIAL_FACEBOOK=https://facebook.com/yourpage
   SOCIAL_TWITTER=https://twitter.com/youraccount
   SOCIAL_INSTAGRAM=https://instagram.com/youraccount
   SOCIAL_YOUTUBE=https://youtube.com/yourchannel

   # Payment Gateways (optional)
   MTN_ENABLED=True
   MTN_API_KEY=your-mtn-api-key
   MTN_SECRET_KEY=your-mtn-secret-key

   # Newsletter Integration (optional)
   MAILCHIMP_API_KEY=your-mailchimp-api-key
   MAILCHIMP_LIST_ID=your-list-id
   ```

**Important Notes:**
- Never commit `.env` file to version control
- Use `.env.example` as a template for documentation
- All sensitive credentials should be stored as environment variables
- For development, you can use default values (check `.env.example`)

### Database
- Development: SQLite (default)
- Production: PostgreSQL (recommended)

To use PostgreSQL:
1. Install psycopg2: `pip install psycopg2-binary`
2. Update `DATABASES` in `settings.py`

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

5. **Run migrations**
   ```bash
   heroku run python manage.py migrate
   ```

### Traditional Server Deployment

1. **Install dependencies on server**
2. **Configure web server** (Nginx + Gunicorn recommended)
3. **Set up SSL certificate**
4. **Configure environment variables**
5. **Run collectstatic**: `python manage.py collectstatic`

## 📱 API Documentation

The project includes Django REST Framework for API functionality:

- **Base URL**: `/api/`
- **Authentication**: Token-based
- **Documentation**: Available at `/api/docs/` (when implemented)

### Key Endpoints
- `/api/auth/` - Authentication
- `/api/users/` - User management
- `/api/trees/` - Tree planting data
- `/api/stats/` - Impact statistics
- `/api/events/` - Event information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `python manage.py test`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Email: info@onecuponetree.org
- Documentation: [Project Wiki](link-to-wiki)
- Issues: [GitHub Issues](link-to-issues)

## 🙏 Acknowledgments

- Bootstrap 5 for responsive design
- Django community for the excellent framework
- Font Awesome for icons
- Unsplash for placeholder images
- All contributors and supporters of the One Cup Initiative

---

**Built with ❤️ for a sustainable future**

## Production `.env` and PostgreSQL

Add a `.env` file at the project root (a template was added as `.env`). Fill in your production values (SECRET_KEY, POSTGRES_*, email credentials, and DJANGO_ALLOWED_HOSTS). Example steps:

```bash
# create and activate virtualenv
python -m venv venv
source venv/bin/activate

# install dependencies (ensure psycopg2-binary and python-dotenv are installed)
pip install -r requirements.txt

# run migrations
python manage.py migrate

# collect static
python manage.py collectstatic --noinput

# run with gunicorn in production
# gunicorn onecup_one_tree_website.wsgi:application --bind 0.0.0.0:8000
```

Keep the `.env` file out of version control and use environment-specific secrets management in production (e.g., server env vars, Docker secrets, or a secret manager).

