pipeline {
  agent any

  environment {
    AWS_REGION = "eu-north-1"
    ECR_URL = "493800112687.dkr.ecr.eu-north-1.amazonaws.com/stockmanager"
    IMAGE_TAG = "${BUILD_NUMBER}"
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Application') {
      steps {
        sh '''
        mvn clean package -DskipTests
        '''
      }
    }


    stage('Build Docker Image') {
      steps {
        sh '''
          docker build -t stockmanager:${IMAGE_TAG} .
          docker tag stockmanager:${IMAGE_TAG} $ECR_URL:${IMAGE_TAG}
        '''
      }
    }

    stage('Push to ECR') {
      steps {
        sh '''
          aws ecr get-login-password --region $AWS_REGION \
          | docker login --username AWS --password-stdin ${ECR_URL%/*}

          docker push $ECR_URL:${IMAGE_TAG}
        '''
      }
    }

    stage('Deploy GREEN') {
      steps {
        sh '''
          sed "s|IMAGE_PLACEHOLDER|$ECR_URL:${IMAGE_TAG}|g" kubernetes/green.yaml \
          | kubectl apply -f -

          kubectl rollout status deployment/stockmanager-green --timeout=180s
        '''
      }
    }

    stage('Health Check GREEN') {
      steps {
        sh '''
          kubectl exec deploy/stockmanager-green -- \
          curl -f http://localhost:8030/health
        '''
      }
    }

    stage('Switch Traffic to GREEN') {
      steps {
        sh '''
          kubectl patch service stockmanager-svc \
          -p '{"spec":{"selector":{"app":"stockmanager","version":"green"}}}'
        '''
      }
    }
  }

  post {
    failure {
      echo "❌ Deployment failed – traffic NOT switched"
    }
    success {
      echo "✅ Green deployment live"
    }
  }
}
