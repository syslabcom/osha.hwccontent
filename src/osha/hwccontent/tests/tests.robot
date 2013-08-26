*** Settings ***

Resource          resource/settings.robot

Suite Setup  Start browser
Suite Teardown  Close All Browsers

*** Variables ***

${BROWSER} =  firefox

*** Test Cases ***

Content editor can add Organisation
    Given I'm logged in as a 'Site Administrator'
      And I add an Organisation
     Then Page Should Contain  The Organisations Title
    