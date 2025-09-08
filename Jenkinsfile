pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-username/flask-react-crud.git'
            }
        }
        
        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'docker build -t your-dockerhub-username/flask-react-crud-backend:latest .'
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'docker build -t your-dockerhub-username/flask-react-crud-frontend:latest .'
                }
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit'
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                        sh 'echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin'
                        sh 'docker push your-dockerhub-username/flask-react-crud-backend:latest'
                        sh 'docker push your-dockerhub-username/flask-react-crud-frontend:latest'
                    }
                }
            }
        }
        
        stage('Deploy with Ansible') {
            steps {
                ansiblePlaybook(
                    playbook: 'ansible/deploy.yml',
                    credentialsId: 'ssh-credentials',
                    inventory: 'ansible/inventory.ini'
                )
            }
        }
    }
    
    post {
        always {
            sh 'docker-compose -f docker-compose.test.yml down'
            cleanWs()
        }
    }
}
