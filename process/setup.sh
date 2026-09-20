#!/bin/bash
# Quick Setup Script for Event Management System

echo "🚀 Setting up Event Management System..."

# Step 1: Create and apply migrations
echo ""
echo "📦 Creating database migrations..."
python manage.py makemigrations

echo ""
echo "📥 Applying migrations..."
python manage.py migrate

# Step 2: Create superuser
echo ""
echo "👤 Creating superuser account..."
echo "Enter superuser details:"
python manage.py createsuperuser

# Step 3: Run development server
echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 Starting development server..."
echo "📍 Access the app at: http://localhost:8000"
echo "📍 Admin panel at: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop the server"
python manage.py runserver
