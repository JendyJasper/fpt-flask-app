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
                echo 'Cloning the repo..'
                sh 'git clone https://github.com/JendyJasper/fpt-flask-app'
            }
        }
        stage('Retrieve Latest Tag') {
            steps {
                script {
                    def awsCliCmd = "aws ecr describe-images --repository-name ${env.ECR_REPOSITORY} --region ${env.AWS_REGION}"
                    def tagsJson = sh(script: awsCliCmd, returnStdout: true).trim()
                    def tags = readJSON text: tagsJson
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
        stage('Build') {
            steps {
                echo 'Building....'
                sh 'docker build -t my_image:${env.COMMIT_HASH} .'
            }
        }
        stage('Push') {
            steps {
                echo 'Pushing....'
                sh 'docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/my-repo/my_image:${env.COMMIT_HASH}'
            }
        }
        stage('Pull & Push k8s Manifest') {
            steps {
                dir('path/to/git/directory') {
                    // Change to the specified directory
                    sh 'git pull origin master'
                    // Pull latest changes from the master branch
                    echo "Latest tag: $latestTag"
                    echo "Latest tag: $COMMIT_HASH"
                    sh "sed -i 's/${env.latestTag}/my_image:${env.COMMIT_HASH}/g' file.txt"
                    // Use sed to make changes in file.txt (replace old_pattern with new_pattern)
                    sh 'git add .'
                    // Stage changes
                    sh 'git commit -m "Image tag updated to ${env.COMMIT_HASH}"'
                    // Commit changes
                    sh 'git push origin master'
                    // Push changes to the master branch
                
                }
            }
        }
    }
}
