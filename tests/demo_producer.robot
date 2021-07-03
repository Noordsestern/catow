*** Settings ***
Library    CamundaLibrary    ${CAMUNDA_HOST}

*** Variables ***
${CAMUNDA_HOST}    http://localhost:8080
${AMOUNT_DEMO_PROCESSES}    3

*** Tasks ***
Create demo processes
    FOR    ${i}    IN RANGE    0    ${AMOUNT_DEMO_PROCESSES}
        start process    simple_demo
    END