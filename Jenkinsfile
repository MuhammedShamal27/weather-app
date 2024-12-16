pipeline {
    agent any

    environment {
        DOCKER_IMAGE_FRONTEND = 'weatherapp-frontend'
        DOCKER_IMAGE_BACKEND = 'weatherapp-backend'
        DOCKER_REGISTRY = 'shamal27'
    }

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['local', 'staging', 'production'], description: 'Select Deployment Environment')
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull the code from GitHub repository
                git 'https://github.com/MuhammedShamal27/weather-app.git'
            }
        }

        stage('Build Frontend') {
            steps {
                script {
                    // Build the frontend Docker image
                    sh 'docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_FRONTEND} ./frontend'
                }
            }
        }

        stage('Build Backend') {
            steps {
                script {
                    // Build the backend Docker image
                    sh 'docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE_BACKEND} ./backend'
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    // Push Docker images to Docker Hub
                    sh 'docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_FRONTEND}'
                    sh 'docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_BACKEND}'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy the application using Docker (docker-compose for local or staging)
                    if (params.ENVIRONMENT == 'local') {
                        sh 'docker-compose -f docker-compose.local.yml up -d'
                    } else if (params.ENVIRONMENT == 'staging') {
                        sh 'docker-compose -f docker-compose.staging.yml up -d'
                    } else if (params.ENVIRONMENT == 'production') {
                        // Commands for production deployment (e.g., Kubernetes, Docker Swarm)
                        echo 'Production deployment logic goes here.'
                    }
                }
            }
        }

        stage('Post-Deployment Testing') {
            steps {
                script {
                    // Run tests to ensure everything is working (you can define your own test script)
                    sh './run_tests.sh'
                }
            }
        }

        stage('Rollback') {
            steps {
                script {
                    // Rollback logic in case deployment fails (use the last good Docker image)
                    if (currentBuild.result == 'FAILURE') {
                        echo 'Deployment failed, rolling back...'
                        // Add your rollback logic here, such as redeploying the previous Docker image
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up resources after the pipeline run
            sh 'docker system prune -f'
        }
    }
}
