pipeline {
    agent any

    environment {
        COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        // Capture the short version of the commit hash using 'git rev-parse --short HEAD'
        OLD_IMAGE_TAG = sh(script: 'git rev-parse --short HEAD^', returnStdout: true).trim()
        // Get the previous commit hash as the old image tag
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '571207880192.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPOSITORY = 'fpt-flask-app'
    }

    stages {
        stage('SCM Checkout') {
            steps {
                // Checkout source code from Git
                git branch: 'main', url: 'https://github.com/JendyJasper/fpt-flask-app.git'
            }
        }
        stage('Retrieve Latest Tag') {
            steps {
                script {
                    def awsCliCmd = "aws ecr describe-images --repository-name ${env.ECR_REPOSITORY} --region ${env.AWS_REGION}"
                    def tagsJson = sh(script: awsCliCmd, returnStdout: true).trim()
                    
                    // Parse JSON using jsonSlurper
                    def jsonSlurper = new groovy.json.JsonSlurper()
                    def tags = jsonSlurper.parseText(tagsJson)
                    
                    def latestTag = tags.imageDetails[0].imageTags[0]
                    echo "Latest tag: $latestTag"
                    // Use the latestTag as needed in subsequent steps
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
                echo 'Loging in....'
                sh 'sudo docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) 571207880192.dkr.ecr.us-east-1.amazonaws.com'
                echo 'login successful..'
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
                sh "sudo docker tag fpt-flask-app:${env.COMMIT_HASH} 571207880192.dkr.ecr.us-east-1.amazonaws.com/fpt-flask-app:${env.COMMIT_HASH}"
            }
        }
        stage('Docker Push') {
            steps {
                echo 'Pushing....'
                sh "sudo docker push 571207880192.dkr.ecr.us-east-1.amazonaws.com/fpt-flask-app:${env.COMMIT_HASH}"
            }
        }
        stage('Pull & Push k8s Manifest') {
            steps {
                dir('/home/ubuntu/fpt-k8s-manifest') {
                    // Change to the specified directory
                    sh 'git pull origin master'
                    // Pull latest changes from the master branch
                    echo "Latest tag: $latestTag"
                    echo "New image tag: $COMMIT_HASH"
                    sh "sed -i 's/${env.latestTag}/${env.COMMIT_HASH}/g' fpt-flask-redis/fpt_flask_app_values.yml"
                    // Use sed to make changes in file.txt (replace old_pattern with new_pattern)
                    sh 'git add .'
                    // Stage changes
                    sh 'git commit -m "Image tag updated to ${env.COMMIT_HASH}"'
                    // Commit changes
                    sh 'git push origin main'
                    // Push changes to the master branch
                
                }
            }
        }
    }
}
