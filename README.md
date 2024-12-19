WeatherApp CI/CD Pipeline Documentation

The aim of the project is to build and secure a frontend-backend application with a Jenkins CI/CD pipeline, using Docker for containerization, self-signed SSL for backend security, and automated post-deployment testing.

1. Application:

Frontend: React.js (Vite)
Backend: Flask (Python)

2. Steps to Configure, Run, and Test Jenkins Pipeline:

Prerequisites:

Jenkins, Docker Desktop, GitHub, Docker Hub account.
Configuration Steps:

Clone the repository:
git clone https://github.com/MuhammedShamal27/weather-app.git
cd weather-app

Configure Jenkins credentials:

Docker Hub: Username & password (ID: dockerhub-creds)
GitHub: Username & token (ID: jenkins-cicd)
SSL Certificates: Add cert-pem & key-pem for certs.

Set up Jenkins pipeline:

New pipeline job: WeatherApp-CI-CD
SCM: GitHub repository URL, use jenkins-cicd credentials, Branch: feature/local-deployment
Set script path to Jenkinsfile.
Add webhooks to automatically trigger Jenkins build on push.

3. Run Frontend and Backend Locally:
   
   Frontend (Vite):
   cd frontend
   npm install
   npm run dev

   Backend (Flask):
   cd backend
   pip install -r requirements.txt
   python app.py
   
Run Jenkins Pipeline:

The Jenkins build is triggered when code is pushed to GitHub, and the webhook notifies Jenkins.

Monitor logs:

Monitor logs in Console Output to ensure the process is successful.

Verify deployment:

Frontend: http://localhost
Backend API: https://localhost:5000/weather

Testing:

API Accessibility: Run curl to https://localhost:5000/weather
Frontend Communication: Run curl to http://localhost
Certificate Verification: Ensure certificates are in /app/certs.

Failure Handling:

Rolls back to the last successful deployment if a test fails.


Note: I couldn't achieve the staging and production deployment as part of the machine task. Despite several attempts, I was unable to successfully set up the production environment.







