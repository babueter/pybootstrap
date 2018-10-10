pipeline {
    agent any

    environment {
        PYTHON = "python3"
    }

    stages {
        stage("Virtual Environment") {
            steps {
                sh """
                    ${env.PYTHON} -m virtualenv .venv --never-download
                    source .venv/bin/activate
                    ${env.PYTHON}
                    ${env.PYTHON} -m pip install -r requirements.txt
                """
            }
        }
        stage("Unit Test") {
            steps {
                sh """
                    source .venv/bin/activate
                    coverage run --source pybootstrap -m unittest discover
                    coverage xml
                """
            }
        }
        post {
            always {
                step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: '**/coverage.xml', failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 0, onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false])
            }
        }
    }
}
