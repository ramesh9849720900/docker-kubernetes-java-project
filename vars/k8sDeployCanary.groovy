
def call() {
    stage('Canary Deployment') {
        sh "kubectl apply -f kubernetes/canary.yaml"
    }
}
