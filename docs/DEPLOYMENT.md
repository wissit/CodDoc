# Deployment Guide

CodDoc AI is designed to be easily deployed to modern cloud platforms. This guide covers deploying the Backend to Railway and Frontend to Vercel.

## Backend Deployment (Railway)

1. **Prerequisites**:
   - Railway Account
   - GitHub Repository with source code

2. **Steps**:
   - Connect your GitHub repo to Railway.
   - Select the `backend` directory as the Root Directory in settings.
   - Add a **PostgreSQL** database service in Railway.
   - Connect the PostgreSQL service to your backend service.
   - Set environment variables:
     - `GEMINI_API_KEY`: Your Google Gemini API key
     - `DATABASE_URL`: (Railway handles this automatically if linked)
     - `PORT`: 8000
   - Railway will automatically detect the `Dockerfile` and build the service.

## Frontend Deployment (Vercel)

1. **Prerequisites**:
   - Vercel Account
   - GitHub Repository

2. **Steps**:
   - Import your GitHub repo in Vercel.
   - Select `Next.js` as the framework preset.
   - Set the Root Directory to `frontend`.
   - Set environment variables:
     - `NEXT_PUBLIC_API_URL`: The URL of your deployed Railway backend (e.g., `https://coddoc-backend.up.railway.app`)
   - Click **Deploy**.

## Docker Deployment (Any VPS)

You can also deploy to any VPS (AWS EC2, DigitalOcean Droplet) using Docker Compose:

1. SSH into your server.
2. Clone the repository.
3. Create `.env` file with production secrets.
4. Run:
   ```bash
   docker-compose up -d --build
   ```
