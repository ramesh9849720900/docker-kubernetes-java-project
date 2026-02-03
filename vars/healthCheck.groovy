
def call(String url) {
    stage('Health Check') {
        sh "curl -f ${url}"
    }
}
