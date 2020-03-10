pipeline {
    agent { dockerfile { filename '.jenkins/Dockerfile' } }
    stages {
        stage('Build') {
            steps {
                sh """
                    tox
                """
            }
        }
        stage('Release') {
            when {
                branch 'master'
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'git_credentials',
                        usernameVariable: 'username',
                        passwordVariable: 'password'
                    )
                ]) {
                    script {
                        version = sh(returnStdout: true, script: "python setup.py --version").trim()
                        sh """
                            git tag $version
                            git push https://$username:$password@github.com/pureport/pureport-ansible-modules $version
                        """
                    }
                }
            }
        }
    }
    post {
        success {
            slackSend(color: '#30A452', message: "SUCCESS: <${env.BUILD_URL}|${env.JOB_NAME}#${env.BUILD_NUMBER}>")
        }
        unstable {
            slackSend(color: '#DD9F3D', message: "UNSTABLE: <${env.BUILD_URL}|${env.JOB_NAME}#${env.BUILD_NUMBER}>")
        }
        failure {
            slackSend(color: '#D41519', message: "FAILED: <${env.BUILD_URL}|${env.JOB_NAME}#${env.BUILD_NUMBER}>")
        }
    }
}
