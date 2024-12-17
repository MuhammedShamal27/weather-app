pipeline {
    agent any

    environment {
        DOCKER_IMAGE_FRONTEND = 'weatherapp-frontend'
        DOCKER_IMAGE_BACKEND = 'weatherapp-backend'
        DOCKER_REGISTRY = 'shamal27' // Docker Hub Username
    }

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['local', 'staging', 'production'], description: 'Select Deployment Environment')
    }

    options {
        // Abort if the pipeline runs for more than 1 hour
        timeout(time: 1, unit: 'HOURS') 
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    echo "Running pipeline for ENVIRONMENT: ${params.ENVIRONMENT}"
                }
            }
        }

        stage('Clean Workspace') {
            steps {
                cleanWs() // Clean workspace before starting
            }
        }

        stage('Checkout') {
            steps {
                // Pull the code from GitHub repository
                echo 'Checking out repository...'
                git branch: 'main', url: 'https://github.com/MuhammedShamal27/weather-app.git'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    // Replace with your actual Docker Hub credentials
                    echo 'Logging in to Docker Hub...'
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    }
                }
            }
        }

        stage('Build Frontend') {
            steps {
                script {
                    echo 'Building frontend Docker image...'
                    sh 'docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_FRONTEND}:latest ./frontend'
                }
            }
        }

        stage('Build Backend') {
            steps {
                script {
                    echo 'Building backend Docker image...'
                    sh 'docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_BACKEND}:latest ./backend'
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    echo 'Pushing Docker images to registry...'
                    sh 'docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_FRONTEND}:latest'
                    sh 'docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_BACKEND}:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Starting deployment for environment: ${params.ENVIRONMENT}"
                    if (params.ENVIRONMENT == 'local') {
                        sh 'docker-compose -f docker-compose.local.yml up -d --build'
                    } else if (params.ENVIRONMENT == 'staging') {
                        sh 'docker-compose -f docker-compose.staging.yml up -d --build'
                    } else if (params.ENVIRONMENT == 'production') {
                        echo 'Production deployment logic goes here.'
                        // Add your Kubernetes, Docker Swarm, or other production deployment script
                    }
                }
            }
        }

        stage('Post-Deployment Testing') {
            steps {
                script {
                    echo 'Running post-deployment tests...'
                    // Replace './run_tests.sh' with your actual test script or commands
                    sh './run_tests.sh'
                }
            }
        }

        stage('Rollback on Failure') {
            when {
                expression { currentBuild.result == 'FAILURE' }
            }
            steps {
                script {
                    echo 'Deployment failed! Rolling back to previous stable state...'
                    // Add rollback logic here, such as using previous Docker images
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
            // Add notifications like email/slack if needed
            // mail to: 'your-email@example.com', subject: 'Build Success', body: 'The Jenkins pipeline succeeded.'
        }

        failure {
            echo 'Pipeline failed. Sending notifications...'
            // Add failure notification logic
            // mail to: 'your-email@example.com', subject: 'Build Failure', body: 'The Jenkins pipeline failed.'
        }

        always {
            echo 'Cleaning up unused Docker resources...'
            sh 'docker system prune -f'
        }
    }
}
