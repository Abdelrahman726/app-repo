pipeline {
  agent any
  environment {
    IMAGE = 'abdelrahman1712/myapp'
    GITOPS_REPO = 'github.com/Abdelrahman726/gitops-repo.git'
  }
  stages {
    stage('Build') {
      steps {
        script {
          env.TAG = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        }
        sh 'docker build -t $IMAGE:$TAG .'
      }
    }
    stage('Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub',
            usernameVariable: 'U', passwordVariable: 'P')]) {
          sh 'echo "$P" | docker login -u "$U" --password-stdin'
          retry(3) {
            sh 'docker push $IMAGE:$TAG'
          }
        }
      }
    }
    
    
    stage('Update GitOps repo') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'github',
            usernameVariable: 'GU', passwordVariable: 'GP')]) {
          sh '''
            rm -rf gitops
            git clone https://$GU:$GP@$GITOPS_REPO gitops
            cd gitops
            sed -i "s|image: .*|image: $IMAGE:$TAG|" myapp/deployment.yaml
            git config user.email "jenkins@lab.local"
            git config user.name "jenkins"
            git commit -am "myapp: image $TAG" || echo "no changes"
            git push
          '''
        }
      }
    }
  }
}
