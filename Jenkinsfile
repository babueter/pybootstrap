pipeline {
    agent any

    environment {
        PYTHON = "python3"
    }

    stages {
        stage("Virtual Environment") {
            steps {
                sh """
                    ${env.PYTHON} -m venv .venv
                    source .venv/bin/activate
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
        stage("Coverage") {
            steps {
                step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: '**/coverage.xml', failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 0, onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false])
            }
        }
    }
}
