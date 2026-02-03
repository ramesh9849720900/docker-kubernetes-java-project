@Library('jenkins-shared-library') _

pipeline {
    agent any

    environment {
        APP_DIR = "shopfront"
        ECR_REPO = "493800112687.dkr.ecr.eu-north-1.amazonaws.com/shopfront"
        IMAGE_TAG = "${BUILD_NUMBER}"
        APP_URL = "http://localhost:8030/health"
    }

    stages {
        stage('Build App') {
            steps {
                buildApp(APP_DIR)
            }
        }

        stage('Docker Build & Push') {
            steps {
                dockerBuildPush(APP_DIR, IMAGE_TAG, ECR_REPO)
            }
        }

        stage('Blue Deployment') {
            steps {
                k8sDeployBlueGreen("blue")
            }
        }

       stage('Health Check') {
            steps {
                healthCheck("stockmanager-blue")
            }
        }


        stage('Green Deployment') {
            steps {
                k8sDeployBlueGreen("green")
            }
        }

        stage('Canary Deployment') {
            steps {
                k8sDeployCanary()
            }
        }
    }
}
