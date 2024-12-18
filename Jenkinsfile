pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') 
        FRONTEND_IMAGE = 'shamal27/weatherapp-frontend:latest'
        BACKEND_IMAGE = 'shamal27/weatherapp-backend:latest'
        FRONTEND_IMAGE_ROLLBACK = 'shamal27/weatherapp-frontend:rollback'
        BACKEND_IMAGE_ROLLBACK = 'shamal27/weatherapp-backend:rollback'
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
                    
                    echo "Tagging previous images as rollback versions..."
                    docker pull %FRONTEND_IMAGE% || echo "No previous frontend image found."
                    docker tag %FRONTEND_IMAGE% %FRONTEND_IMAGE_ROLLBACK%
                    docker push %FRONTEND_IMAGE_ROLLBACK%

                    docker pull %BACKEND_IMAGE% || echo "No previous backend image found."
                    docker tag %BACKEND_IMAGE% %BACKEND_IMAGE_ROLLBACK%
                    docker push %BACKEND_IMAGE_ROLLBACK%
                    
                    docker push %FRONTEND_IMAGE%
                    docker push %BACKEND_IMAGE%
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    if (params.ENV == 'production') {
                        echo "Deploying to production..."
                        withCredentials([file(credentialsId: 'production-pem', variable: 'PROD_PEM_FILE')]) {
                            bat '''
                            echo "Deploying to the production server..."
                            echo "PEM file path: %PROD_PEM_FILE%"
                            dir %PROD_PEM_FILE%
                            type %PROD_PEM_FILE%

                            echo "Adjusting permissions on the PEM file..."
                            icacls "%PROD_PEM_FILE%" /inheritance:r
                            icacls "%PROD_PEM_FILE%" /remove "BUILTIN\\Users"
                            REM Change SYSTEM to the actual user Jenkins runs as, if different.
                            icacls "%PROD_PEM_FILE%" /grant:r "NT AUTHORITY\\SYSTEM":F
                            icacls "%PROD_PEM_FILE%"

                            "C:\\Windows\\System32\\OpenSSH\\ssh.exe" -v -o StrictHostKeyChecking=no -i "%PROD_PEM_FILE%" ubuntu@51.20.243.232 "cd /home/ubuntu/weatherapp && docker-compose -f docker-compose.production.yml down && docker-compose -f docker-compose.production.yml up -d"
                            '''
                        }
                    } else {
                        echo "Deploying to local environment..."
                        bat '''
                        docker-compose down
                        docker-compose up -d
                        '''
                    }
                }
            }
        }
        stage('Testing') {
            steps {
                echo "Running post-deployment tests..."
                script {
                    if (params.ENV == 'production') {
                        sh '''
                        echo "Testing backend HTTPS API on production..."
                        curl -k --ssl-no-revoke https://royalsofa.online:5000/weather || exit 1

                        echo "Testing frontend communication on production..."
                        curl -v -k --ipv4 http://royalsofa.online || exit 1
                        '''
                    } else {
                        bat '''
                        docker exec weatherapp-backend ls /app/certs
                        echo Testing backend HTTPS API locally...
                        curl -k --ssl-no-revoke https://localhost:5000/weather || exit /b 1
                        echo Testing frontend communication locally...
                        curl -v -k --ipv4 http://localhost || exit /b 1
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            script {
                echo "Pipeline failed! Rolling back to the last successful deployment..."
                if (params.ENV == 'production') {
                    echo "Rolling back production environment..."
                    bat '''
                    ssh -i S:/DOWNLOADS/production.pem ubuntu@51.20.243.232 "
                    cd /home/ubuntu/weatherapp &&
                    docker-compose -f docker-compose.production.yml down &&
                    docker pull %FRONTEND_IMAGE_ROLLBACK% &&
                    docker pull %BACKEND_IMAGE_ROLLBACK% &&
                    docker tag %FRONTEND_IMAGE_ROLLBACK% %FRONTEND_IMAGE% &&
                    docker tag %BACKEND_IMAGE_ROLLBACK% %BACKEND_IMAGE% &&
                    docker-compose -f docker-compose.production.yml up -d
                    "
                    '''
                } else {
                    echo "Rolling back local environment..."
                    bat '''
                    docker-compose down
                    docker pull %FRONTEND_IMAGE_ROLLBACK%
                    docker pull %BACKEND_IMAGE_ROLLBACK%
                    docker tag %FRONTEND_IMAGE_ROLLBACK% %FRONTEND_IMAGE%
                    docker tag %BACKEND_IMAGE_ROLLBACK% %BACKEND_IMAGE%
                    docker-compose up -d
                    '''
                }
            }
        }
    }
}
