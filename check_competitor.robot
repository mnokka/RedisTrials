*** Settings ***
Library           RequestsLibrary
Library           Collections

*** Variables ***
${BASE_URL}       http://localhost:5000
${BIB_NUMBER}     123
${EXPECTED_STATUS}   200
${EXPECTED_MESSAGE}  Competitor data OK

*** Test Cases ***
Check Competitor Exists and Is Valid
    [Documentation]    Check competitor exist.
    ${response}=      GET  ${BASE_URL}/check_competitor/${BIB_NUMBER}
    Should Be Equal As Numbers    ${response.status_code}    ${EXPECTED_STATUS}
   
    ${json}=    Convert To Dictionary    ${response.json()}
    Should Contain    ${json}    message
    Should Be Equal As Strings    ${json}[message]    ${EXPECTED_MESSAGE}
