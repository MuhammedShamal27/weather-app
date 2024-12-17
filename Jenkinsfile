pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // Docker Hub credentials ID
        FRONTEND_IMAGE = 'shamal27/weatherapp-frontend:latest'
        BACKEND_IMAGE = 'shamal27/weatherapp-backend:latest'
    }

    parameters {
        choice(name: 'ENV', choices: ['local', 'staging', 'production'], description: 'Choose deployment environment')
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out code from GitHub..."
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/MuhammedShamal27/weather-app.git',
                        credentialsId: 'jenkins-cicd'
                    ]]
                ])
            }
        }

        stage('Build') {
            parallel {
                stage('Build Frontend') {
                    steps {
                        echo "Building the frontend..."
                        dir('frontend') {
                            bat '''
                            npm install
                            npm run build
                            '''
                        }
                    }
                }
                stage('Build Backend') {
                    steps {
                        echo "Building the backend..."
                        dir('backend') {
                            withCredentials([
                                file(credentialsId: 'cert-pem', variable: 'CERT_PEM_FILE'),
                                file(credentialsId: 'key-pem', variable: 'KEY_PEM_FILE')
                            ]) {
                                script {
                                    bat '''
                                    echo "Copying certificate files to certs directory..."
                                    if not exist certs mkdir certs
                                    copy %CERT_PEM_FILE% certs\\cert.pem
                                    copy %KEY_PEM_FILE% certs\\key.pem
                                    dir certs
                                    type certs\\cert.pem
                                    type certs\\key.pem
                                    '''
                                }
                            }
                            bat '''
                            echo "Installing Python dependencies..."
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                            '''
                        }
                    }
                }

            }
        }
        stage('Dockerize') {
            steps {
                echo "Building Docker images..."
                bat '''
                docker build -t %FRONTEND_IMAGE% ./frontend
                docker build -t %BACKEND_IMAGE% ./backend
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Pushing Docker images to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                    echo|set /p="%DOCKER_PASS%" | docker login -u %DOCKER_USER% --password-stdin
                    docker push %FRONTEND_IMAGE%
                    docker push %BACKEND_IMAGE%
                    '''
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                echo "Deploying application using Docker Compose..."
                bat '''
                docker-compose down
                docker-compose up -d
                
                '''
            }
        }

        stage('Testing') {
            steps {
                echo "Running post-deployment tests..."
                bat '''
                docker exec weatherapp-backend ls /app/certs
                dir certs
                type certs\\cert.pem
                type certs\\key.pem
                
                echo Testing backend HTTPS API...
                
                echo Testing frontend communication...
                curl -v -k --ipv4 http://localhost || exit /b 1
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
            bat '''
            docker-compose logs backend --tail=100
            '''
        }
        failure {
            echo "Pipeline failed! Rolling back..."
            bat '''
            docker-compose down
            echo Rollback complete. Deployment stopped.
            '''
        }
    }
}
