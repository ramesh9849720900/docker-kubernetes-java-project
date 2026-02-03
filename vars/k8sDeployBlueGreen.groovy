
def call(String color) {
    stage("${color.toUpperCase()} Deployment") {
        sh "kubectl apply -f kubernetes/${color}.yaml"
    }
}
