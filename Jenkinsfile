pipeline {
    agent any

    environment {
        COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '571207880192.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPOSITORY = 'fpt-flask-app'
    }

    stages {
        stage('SCM Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/JendyJasper/fpt-flask-app.git'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing..'
                echo 'Hello World!'
            }
        }

        stage('Docker Login') {
            steps {
                echo 'Logging in....'
                sh 'sudo docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) 571207880192.dkr.ecr.us-east-1.amazonaws.com'
                echo 'Login successful..'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building....'
                sh "sudo docker build -t fpt-flask-app:${env.COMMIT_HASH} ."
            }
        }
        stage('Docker Tag') {
            steps {
                echo 'Tagging image....'
                sh "sudo docker tag fpt-flask-app:${env.COMMIT_HASH} ${env.ECR_REGISTRY}/fpt-flask-app:${env.COMMIT_HASH}"
            }
        }
        stage('Docker Push') {
            steps {
                echo 'Pushing....'
                sh "sudo docker push ${env.ECR_REGISTRY}/fpt-flask-app:${env.COMMIT_HASH}"
                sh "sudo docker rmi -f \$(sudo docker images -q)"
            }
        }
    }
}
