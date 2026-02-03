
/*def call(String url) {
    stage('Health Check') {
        sh "curl -f ${url}"
    }
}
*/

def call(String deploymentName = "stockmanager-blue") {
    sh """
      kubectl rollout status deployment/${deploymentName} --timeout=120s
    """
}
