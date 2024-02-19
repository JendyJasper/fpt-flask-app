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
       stage('Retrieve Last Pushed Image') {
            steps {
                script {
                    def awsCliCmd = "aws ecr describe-images --repository-name ${env.ECR_REPOSITORY} --region ${env.AWS_REGION}"
                    def tagsJson = sh(script: awsCliCmd, returnStdout: true).trim()
                    
                    // Debugging: Print out the tagsJson
                    echo "tagsJson: $tagsJson"
                    
                    // Parse JSON using Groovy's JsonSlurper
                    def jsonSlurper = new groovy.json.JsonSlurper()
                    def tags = jsonSlurper.parseText(tagsJson)
                    
                    // Convert the parsed JSON data into a JSON string and print it
                    echo "Parsed JSON data structure: ${groovy.json.JsonOutput.toJson(tags)}"
                    
                    // Sort the image details by imagePushedAt timestamp
                    def sortedTags = tags.imageDetails.sort { a, b -> a.imagePushedAt <=> b.imagePushedAt }
                    
                    // Check if sortedTags is a list and not empty
                    if (sortedTags instanceof List && !sortedTags.isEmpty()) {
                        // Reverse the order of sortedTags
                        sortedTags = sortedTags.reverse()
                        
                        // Extract the image tag from the first entry
                        def lastImageTag = sortedTags[0].imageTags[0]
                        
                        echo "Last pushed image tag: $lastImageTag"
                    } else {
                        echo "No images found in the repository"
                    }
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
                sh "sudo docker rmi -f \$(sudo docker images -q)"
            }
        }
        stage('Pull & Push k8s Manifest') {
            steps {
                    echo "Latest tag: $LATEST_TAG"
                    git branch: 'main', credentialsId: 'b4dd1a48-6ef2-4468-a130-0a46f7710175', url: 'https://github.com/JendyJasper/fpt-k8s-manifest.git'
                    sh 'git pull origin main'
                    echo "New image tag: ${env.COMMIT_HASH}"
                    sh "sed -i 's/$LATEST_TAG/${env.COMMIT_HASH}/g' fpt-flask-redis/fpt_flask_app_values.yml"
                    sh 'git add fpt-flask-redis/fpt_flask_app_values.yml'
                    sh "git commit -m 'Image tag updated to ${env.COMMIT_HASH}' -a"
                    sh 'git push origin main'
            }
        }
    }
}
