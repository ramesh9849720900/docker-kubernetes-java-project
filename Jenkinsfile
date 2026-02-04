@Library('jenkins-shared-library') _

pipeline {
    agent any

    environment {
        APP_DIR = "shopfront"
        ECR_REPO = "493800112687.dkr.ecr.eu-north-1.amazonaws.com/shopfront"
        IMAGE_TAG = "${BUILD_NUMBER}"
        APP_URL = "http://localhost:8010/health"
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
                sh '''
                kubectl rollout status deployment/stockmanager-blue --timeout=120s
                kubectl port-forward deployment/stockmanager-blue 8010:8010 &
                sleep 10
                curl -f http://localhost:8010/health
                '''
            }
        }


        stage('Green Deployment') {
            steps {
                k8sDeployBlueGreen("green")
            }
        }


         stage('Health Check') {
            steps {
                sh '''
                kubectl rollout status deployment/stockmanager-green --timeout=120s
                kubectl port-forward deployment/stockmanager-green 8010:8010 &
                sleep 10
                curl -f http://localhost:8010/health
                '''
            }
        }


        
        stage('Debug Kube Access') {
            steps {
                sh '''
                whoami
                kubectl config current-context
                kubectl get nodes
                '''
            }
        }


        stage('Canary Deployment') {
            steps {
                k8sDeployCanary()
            }
        }
    }
}
