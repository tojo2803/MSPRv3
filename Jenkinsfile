pipeline {
    agent any

    environment {
        SONARQUBE = 'SonarQube' // Doit correspondre EXACTEMENT au nom du serveur SonarQube dans Jenkins > Manage Jenkins > Configure System
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/tojo2803/MSPRv3.git', branch: 'main'
            }
        }

       stage('SonarQube Analysis') {
    steps {
        script {
            def scannerHome = tool 'SonarScanner' // Use the name you configured in Jenkins Tools
            withSonarQubeEnv("${SONARQUBE}") {
                withCredentials([string(credentialsId: 'SONAR_AUTH_TOKEN', variable: 'SONAR_TOKEN')]) {
                    sh "${scannerHome}/bin/sonar-scanner \\
                        -Dsonar.projectKey=mspr \\
                        -Dsonar.sources=. \\
                        -Dsonar.host.url=http://localhost:9000 \\
                        -Dsonar.login=$SONAR_TOKEN"
                }
            }
        }
    }
}
        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}
