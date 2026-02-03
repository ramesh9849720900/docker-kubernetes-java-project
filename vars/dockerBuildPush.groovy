
def call(String appDir, String imageTag, String ecrRepo) {
    stage('Docker Build & Push') {
        dir(appDir) {
            sh """
              docker build -t ${ecrRepo}:${imageTag} .
              aws ecr get-login-password --region eu-north-1 \
                | docker login --username AWS --password-stdin ${ecrRepo}
              docker push ${ecrRepo}:${imageTag}
            """
        }
    }
}
