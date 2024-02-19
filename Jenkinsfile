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
                    // Execute AWS CLI command to retrieve latest tag
                    def awsCliCmd = "aws ecr describe-images --repository-name ${env.ECR_REPOSITORY} --region ${env.AWS_REGION}"
                    def tagsJson = sh(script: awsCliCmd, returnStdout: true).trim()
                    
                    // Parse JSON response using JsonSlurper
                    def jsonSlurper = new groovy.json.JsonSlurper()
                    def tags = jsonSlurper.parseText(tagsJson)
                    
                    // Assign the latest tag to a variable
                    def latestTag = tags.imageDetails[0].imageTags[0]
                    
                    // Set the latest tag as an environment variable
                    LATEST_TAG = latestTag
                    
                    // Print the latest tag for verification
                    echo "Latest tag: $LATEST_TAG"
                }
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
                    echo "Latest tag: $LATEST_TAG"
                    git branch: 'main', credentialsId: 'b4dd1a48-6ef2-4468-a130-0a46f7710175', url: 'https://github.com/JendyJasper/fpt-k8s-manifest.git'
                    sh 'sudo git pull origin main'
                    echo "New image tag: ${env.COMMIT_HASH}"
                    sh "sed -i 's/$LATEST_TAG/${env.COMMIT_HASH}/g' fpt-flask-redis/fpt_flask_app_values.yml"
                    sh 'sudo git add .'
                    sh 'sudo git commit -m "Image tag updated to ${env.COMMIT_HASH}"'
                    sh 'sudo git push origin main'
                }
            }
        }
    }
}
