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
                """
            }
        }
        stage("Coverage") {
            steps {
                sh """
                    source .venv/bin/activate
                    coverage xml
                """
            }
        }
    }
}