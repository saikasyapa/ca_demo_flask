# Cloud Automation Flask Demo

A Flask web application with MySQL database for product management with full CRUD operations.

## Features

- Flask web framework
- MySQL database integration
- Bootstrap 5 UI
- CRUD operations (Create, Read, Update, Delete)
- Docker containerization

## Local Development

### Prerequisites
- Python 3.9+
- MySQL Server
- pip

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup
```bash
# Make sure MySQL is running
python setup_db.py
```

### Running
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and run the application with MySQL
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Using Docker directly

```bash
# Build the image
docker build -t ca-demo-flask .

# Run with MySQL (requires separate MySQL container)
docker run -p 5000:5000 \
  -e DB_HOST=host.docker.internal \
  -e DB_USER=root \
  -e DB_PASSWORD=your_password \
  -e DB_NAME=ca_demo \
  --name ca-demo-flask \
  ca-demo-flask
```

## Environment Variables

- `DB_HOST`: MySQL host (default: localhost)
- `DB_USER`: MySQL username (default: root)
- `DB_PASSWORD`: MySQL password
- `DB_NAME`: Database name (default: ca_demo)
- `FLASK_ENV`: Environment (development/production)

## Docker Commands

```bash
# Check container status
docker-compose ps

# View container logs
docker-compose logs ca-demo-flask

# Access MySQL container
docker-compose exec mysql mysql -u root -p ca_demo

# Stop services
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v
```

## AWS EC2 Deployment

### Prerequisites
- AWS Account with EC2 access
- SSH key pair for EC2 instance access
- Basic knowledge of AWS console or AWS CLI

### Step 1: Launch EC2 Instance

1. **Log in to AWS Console** and navigate to EC2 service
2. **Click "Launch Instance"**
3. **Choose AMI**: Amazon Linux 2 or Ubuntu Server (latest LTS)
4. **Instance Type**: t2.small or t3.small (Flask + MySQL needs more resources than simple apps)
5. **Configure Security Group**:
   - Add rule: HTTP (port 80) from 0.0.0.0/0
   - Add rule: SSH (port 22) from your IP or 0.0.0.0/0
   - Add rule: Custom TCP (port 5000) from 0.0.0.0/0 (for direct access)
6. **Storage**: Increase to at least 20GB for database storage
7. **Launch the instance** and note the Public IP/DNS

### Step 2: Connect to EC2 Instance

```bash
# Connect using SSH (replace with your key and instance details)
ssh -i your-key.pem ec2-user@your-instance-public-ip

# For Ubuntu instances, use:
ssh -i your-key.pem ubuntu@your-instance-public-ip
```

### Step 3: Install Docker on EC2

```bash
# Update system packages
sudo yum update -y  # For Amazon Linux
# OR for Ubuntu:
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo yum install -y docker  # Amazon Linux
# OR for Ubuntu:
sudo apt install -y docker.io

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add current user to docker group (optional)
sudo usermod -aG docker $USER
# Logout and login again for group changes to take effect
```

### Step 4: Install Git and Clone Repository

```bash
# Install Git
sudo yum install -y git  # Amazon Linux
# OR for Ubuntu:
sudo apt install -y git

# Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name/ca_demo_flask
```

### Step 5: Run the Application

```bash
# Build and run with Docker Compose (includes MySQL database)
sudo docker-compose up -d

# Wait for MySQL to be ready (check with docker-compose logs)
sudo docker-compose logs -f mysql
```

### Step 6: Configure Nginx (Optional - for production)

```bash
# Install Nginx
sudo yum install -y nginx  # Amazon Linux
# OR for Ubuntu:
sudo apt install -y nginx

# Create Nginx configuration
sudo tee /etc/nginx/conf.d/ca_demo_flask.conf > /dev/null <<EOF
server {
    listen 80;
    server_name your-instance-public-ip;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Step 7: Access Your Application

- **Direct access**: http://your-instance-public-ip:5000
- **Through Nginx**: http://your-instance-public-ip (if configured)

### Database Management

```bash
# Access MySQL database
sudo docker-compose exec mysql mysql -u root -p ca_demo

# View database logs
sudo docker-compose logs mysql

# Backup database (if needed)
sudo docker-compose exec mysql mysqldump -u root -p ca_demo > backup.sql
```

### Monitoring and Management

```bash
# Check all service status
sudo docker-compose ps

# View application logs
sudo docker-compose logs -f flask

# View all logs
sudo docker-compose logs -f

# Stop the application
sudo docker-compose down

# Update the application
git pull
sudo docker-compose up -d --build
```

### Troubleshooting

- **Port not accessible**: Check security group rules in AWS console
- **MySQL connection failed**: Wait for MySQL container to fully initialize
- **Container not starting**: Check logs with `docker-compose logs`
- **Memory issues**: Flask + MySQL needs adequate RAM, consider t3.small or larger
- **Database data lost**: Data persists in Docker volumes unless removed with `-v` flag

### Cost Optimization

- Use t2.small for development/testing
- Stop instances when not in use to save costs
- Consider RDS for production database instead of containerized MySQL
- Set up auto-scaling groups for production workloads
- Use EBS snapshots for database backups

## Database Schema

The application uses a `products` table:
- `id` (INT, Primary Key, Auto Increment)
- `name` (VARCHAR(255))
- `description` (TEXT)
- `price` (DECIMAL(10,2))
- `created_at` (TIMESTAMP)

## Project Structure

```
ca_demo_flask/
├── app.py                 # Main Flask application
├── setup_db.py           # Database setup script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── templates/            # Jinja2 templates
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Docker ignore file
├── nginx/                # Nginx configuration
└── README.md            # This file
```

## API Endpoints

- `GET /`: List all products
- `GET /product/<id>`: View product details
- `GET/POST /add`: Add new product
- `GET/POST /edit/<id>`: Edit product
- `POST /delete/<id>`: Delete product

## Technologies Used

- **Runtime**: Python 3.9
- **Framework**: Flask
- **Database**: MySQL 8.0
- **ORM**: Raw SQL queries
- **Frontend**: Bootstrap 5, Jinja2
- **Container**: Docker
- **Orchestration**: Docker Compose

## Database Schema

The application uses a `products` table with the following structure:
- `id` (INT, Primary Key, Auto Increment)
- `name` (VARCHAR(255))
- `description` (TEXT)
- `price` (DECIMAL(10,2))
- `created_at` (TIMESTAMP)

## Project Structure

```
ca_demo_flask/
├── app.py                 # Main Flask application
├── setup_db.py           # Database setup script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add_product.html
│   └── product_detail.html
└── README.md
```

## Technologies Used

- **Backend:** Flask (Python web framework)
- **Database:** MySQL
- **Frontend:** Bootstrap 5, Jinja2 templates
- **Other:** python-dotenv for environment management