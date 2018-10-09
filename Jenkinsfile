pipeline {
    agent any

    stages {
        unit_test {
            sh "coverage run --source pybootstrap -m unittest discover"
        }
        coverage {
            sh "coverage xml"
        }
    }
}