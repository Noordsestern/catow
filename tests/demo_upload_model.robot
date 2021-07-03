*** Settings ***
Library    CamundaLibrary    ${CAMUNDA_HOST}

*** Variables ***
${CAMUNDA_HOST}    http://localhost:8080

*** Tasks ***
Upload demo model
    deploy    ${CURDIR}/bpmn/diagram_1.bpmn