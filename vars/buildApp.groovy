
def call(String appDir) {
    stage('Build') {
        dir(appDir) {
            sh 'mvn clean package -DskipTests'
        }
    }
}
