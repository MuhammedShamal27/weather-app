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

        stage('Deploy') {
            steps {
                script {
                    if (params.ENV == 'production') {
                        echo "Deploying to production..."
                        bat '''
                        ssh -i production.pem ubuntu@51.20.243.232 "cd /home/ubuntu/weatherapp && docker-compose -f docker-compose.production.yml down && docker-compose -f docker-compose.production.yml up -d"
                        '''
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
                if (params.ENV == 'production') {
                    echo "Pipeline failed! Rolling back production deployment..."
                    sh '''
                    ssh -i production.pem ubuntu@51.20.243.232 '
                    cd /home/ubuntu/weatherapp &&
                    docker-compose -f docker-compose.production.yml down &&
                    echo "Rollback complete. Production deployment stopped."
                    '
                    '''
                } else {
                    echo "Pipeline failed! Rolling back local deployment..."
                    bat '''
                    docker-compose down
                    echo Rollback complete. Local deployment stopped.
                    '''
                }
            }
        }
    }
}
