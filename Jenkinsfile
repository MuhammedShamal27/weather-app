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
                                string(credentialsId: 'cert-pem', variable: 'CERT_PEM'),  
                                string(credentialsId: 'key-pem', variable: 'KEY_PEM')     
                            ]) {
                                script {
                                    bat '''
                                    mkdir certs
                                    echo %CERT_PEM% > certs/cert.pem
                                    echo %KEY_PEM% > certs/key.pem
                                    '''
                                    bat '''
                                    python -m pip install --upgrade pip
                                    pip install -r requirements.txt
                                    '''                                    
                                    bat 'docker build -t %BACKEND_IMAGE% ./backend'
                                }
                            }
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
                    docker push shamal27/weatherapp-frontend:latest
                    docker push shamal27/weatherapp-backend:latest
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
                echo Testing backend HTTPS API...
                curl -k --ssl-no-revoke https://localhost:5000/weather || exit /b 1

                echo Testing frontend communication...
                curl -k http://localhost || exit /b 1
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
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
