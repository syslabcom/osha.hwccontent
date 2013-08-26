*** Keywords ***
Open Menu
    [Arguments]  ${elementId}

    Element Should Be Visible  css=dl#${elementId} span
    Element Should Not Be Visible  css=dl#${elementId} dd.actionMenuContent
    Click link  css=dl#${elementId} dt.actionMenuHeader a
    Wait until keyword succeeds  1  5  Element Should Be Visible  css=dl#${elementId}  dd.actionMenuContent

Open Add New Menu
    Open Menu  plone-contentmenu-factories

I'm logged in as a '${ROLE}'
    Enable autologin as  ${ROLE}
    Go to  ${PLONE_URL}

I disable WYSIWYG editor
    Goto  ${PLONE_URL}/@@personal-preferences
    Select from list  form.wysiwyg_editor  None
    Click Button  Save
    
I open the personal menu
    Click link  css=#user-name

I see the Site Setup -link
    Element should be visible  css=#personaltools-plone_setup


I add a Test Definition
    Open Add New Menu
    Click link  densoqs-content-testdefinition
    Page Should Contain  HVAC
    Click link  HVAC
    Click link  Vibration requirements
    Click link  Running Smoothness
    Click element  //span[contains(@class,"dynatree-focused")]/span[@class="dynatree-checkbox"]
    Input Text  form.widgets.specification_number  EKE-7-T-PANG
    Input Text  form.widgets.release_date-day  5
    Select from list  form.widgets.release_date-month  7
    Input Text  form.widgets.release_date-year  2013
    Input Text  form.widgets.test_number  4711
    Select from list  form.widgets.test_location:list  Bench
    Input Text  form.widgets.test_procedure  Test procedure
    Input Text  form.widgets.specification  Lorem ipsum
    Click Button  Save
    Page Should Contain  Item created
    