pipeline {
    agent any

    stages {
        stage("Unit Test") {
            steps {
                sh "coverage run --source pybootstrap -m unittest discover"
            }
        }
        stage("Coverage") {
            steps {
                sh "coverage xml"
            }
        }
    }
}