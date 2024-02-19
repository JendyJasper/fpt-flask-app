pipeline {
    agent any

    environment {
        COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        OLD_IMAGE_TAG = sh(script: 'git rev-parse --short HEAD^', returnStdout: true).trim()
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '571207880192.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPOSITORY = 'fpt-flask-app'
        LATEST_TAG = ''
    }

    stages {
        stage('SCM Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/JendyJasper/fpt-flask-app.git'
            }
        }
        stage('Retrieve Latest Tag') {
            steps {
                script {
                    def awsCliCmd = "aws ecr describe-images --repository-name ${env.ECR_REPOSITORY} --region ${env.AWS_REGION}"
                    def tagsJson = sh(script: awsCliCmd, returnStdout: true).trim()
                    def jsonSlurper = new groovy.json.JsonSlurper()
                    def tags = jsonSlurper.parseText(tagsJson)
                    LATEST_TAG = tags.imageDetails[0].imageTags[0]
                    echo "Latest tag: $LATEST_TAG"
                }
            }
        }
        stage('Test Latest Tag') {
            steps {
                echo "Latest tag from Test stage: ${env.LATEST_TAG}"
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
            }
        }
        stage('Pull & Push k8s Manifest') {
            steps {
                dir('/home/ubuntu/fpt-k8s-manifest') {
                    echo "Latest tag: ${env.LATEST_TAG}"
                    sh 'git pull origin main'
                    echo "New image tag: ${env.COMMIT_HASH}"
                    sh "sed -i 's/${env.LATEST_TAG}/${env.COMMIT_HASH}/g' fpt-flask-redis/fpt_flask_app_values.yml"
                    sh 'git add .'
                    sh 'git commit -m "Image tag updated to ${env.COMMIT_HASH}"'
                    sh 'git push origin main'
                }
            }
        }
    }
}
