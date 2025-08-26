# One Cup One Tree Initiative Website

A comprehensive Django web application for the One Cup One Tree Initiative - a sustainable movement empowering farmers, training youth, and restoring our planet through innovative coffee and tree planting programs.

## 🌟 Features

### Core Functionality
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **User Authentication**: Role-based access control (Admin, Partner, Donor, Volunteer, Visitor, Student)
- **Multilingual Support**: English, French, and Kinyarwanda
- **Impact Tracking**: Real-time statistics for trees planted, youth trained, and environmental impact

### Programs
- **Coffee Farmer Support**: Seedling distribution, training, and market access
- **Youth Barista Academy**: Comprehensive training programs with scholarship opportunities
- **One Cup One Tree Campaign**: Tree planting tracking with digital certificates

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

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the website**
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
- Modify colors in `templates/base.html` CSS section
- Primary color: `#2d5016` (forest green)
- Secondary color: `#8b4513` (coffee brown)

#### Content
- Update site settings in `settings.py`
- Modify homepage content in `apps/core/views.py`
- Edit templates in `templates/` directory

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost/dbname

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment gateways
MTN_API_KEY=your-mtn-api-key
RWANDA_PAY_API_KEY=your-rwandapay-api-key
PAYPAL_CLIENT_ID=your-paypal-client-id

# Newsletter
MAILCHIMP_API_KEY=your-mailchimp-api-key
MAILCHIMP_LIST_ID=your-list-id
```

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
- All contributors and supporters of the One Cup One Tree Initiative

---

**Built with ❤️ for a sustainable future**

