pipeline {
    agent any

    environment {
        DOCKER_IMAGE = '698subhashchandra/credit-rating-api:latest'
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_CREDENTIALS = 'dockerhub-cred'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clean workspace before cloning
                cleanWs()
                git branch: 'main',
                    url: 'https://github.com/698subhashchandra/credit-rating-api1.git'

                echo "Repository cloned successfully"
            }
        }

        stage('Docker Login and Pull Image') {
            steps {
                script {
                    // Use credentials to login to DockerHub
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "docker login -u $DOCKER_USER -p $DOCKER_PASS ${DOCKER_REGISTRY}"
                    }
                    // Pull the Docker image
                    sh "docker pull ${DOCKER_IMAGE}"
                    echo "Docker image pulled successfully"
                }
            }
        }

        stage('Run Application') {
            steps {
                script {
                    // Run the Docker container with proper port mapping
                    sh "docker run -d -p 8000:8000 ${DOCKER_IMAGE}"
                    echo "Application is running successfully"
                }
            }
        }

        stage('Verify Application') {
            steps {
                echo "==================================================="
                echo "             Application is running                  "
                echo "==================================================="
                // Add commands to validate the application if necessary
            }
        }
    }

    post {
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check the logs for details."
        }
    }
}
