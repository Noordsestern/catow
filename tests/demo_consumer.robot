*** Settings ***
Library    CamundaLibrary    ${CAMUNDA_HOST}

*** Variables ***
${CAMUNDA_HOST}    http://localhost:8080

*** Tasks ***
Process demo workload
    Fetch workload    aTopic
    Complete task