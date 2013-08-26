*** Settings ***

Resource          resource/settings.robot

Suite Setup  Start browser
Suite Teardown  Close All Browsers

*** Variables ***

${BROWSER} =  firefox

*** Test Cases ***

Content editor can add Organisation
    Given I'm logged in as a 'Site Administrator'
    Go to  http://localhost:55001/plone/
    Page should contain  Plone site
    

*** Keywords ***

Start browser
    Open browser  http://localhost:55001/plone/  browser=${BROWSER}
