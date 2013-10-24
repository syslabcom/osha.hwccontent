*** Keywords ***
Start browser
    Open browser  ${PLONE_URL}  browser=${BROWSER}

Test Setup
    Start browser
    I'm logged in as a 'Site Administrator'
    I add an Organisations folder
    Go to  ${PLONE_URL}

Open Menu
    [Arguments]  ${elementId}

    Element Should Be Visible  css=dl#${elementId} span
    Element Should Not Be Visible  css=dl#${elementId} dd.actionMenuContent
    Click link  css=dl#${elementId} dt.actionMenuHeader a
    Wait until keyword succeeds  1  5  Element Should Be Visible  css=dl#${elementId}  dd.actionMenuContent

Open Add New Menu
    Open Menu  plone-contentmenu-factories

I'm logged in as a ${ROLE}
    Go to  ${PLONE_URL}/login_form
    Input text  __ac_name  ${ROLE}
    Input text  __ac_password  password
    Click button  Log in
    Page should contain  You are now logged in
    Go to  ${PLONE_URL}

I logout
    Go to  ${PLONE_URL}/logout
    Page should contain  You are now logged out

I'm logged out
    Page should contain  Log in

I disable WYSIWYG editor
    Goto  ${PLONE_URL}/@@personal-preferences
    Select from list  form.wysiwyg_editor  None
    Click Button  Save
    
I see the Site Setup -link
    Element should be visible  css=#personaltools-plone_setup

I go to the Organisations folder
    Click link  Organisations

I add an Organisations folder
    Goto  ${PLONE_URL}/++add++osha.hwccontent.organisationfolder
    Page Should Contain  Organisation Folder
    Input Text           form.widgets.IDublinCore.title       Organisations
    Click Button  Save
    Page Should Contain  Item created
    Page Should Contain  Organisations

I register an Organisation
    Open Add New Menu
    Click link  css=#osha-hwccontent-organisation
    Page Should Contain  Organisation
    Input Text           form.widgets.IDublinCore.title  The Organisations Title
    Input Text           form.widgets.street             O Street
    Input Text           form.widgets.city               Osterburg
    Input Text           form.widgets.zip_code           12345
    Select from list     form.widgets.country:list       Iceland
    Input Text           form.widgets.email              email@organisation.org
    Input Text           form.widgets.phone              012346789
    Input Text           form.widgets.url                http://www.organisation.org/
    Input Text           form.widgets.campaign_url       http://www.organisation.org/
    Choose File          form.widgets.logo               ${CURDIR}/logo.gif
    Input Text           form.widgets.organisation_type  Organised
    Input Text           form.widgets.business_sector    Organisation
    Input Text           form.widgets.mission_statement  We organise you!
    Input Text           form.widgets.campaign_pledge    Making you even more organised!
    Choose File          form.widgets.ceo_image          ${CURDIR}/ceo.jpg
    Input Text           form.widgets.ceo_name           Odina Organiser
    Input Text           form.widgets.ceo_position       CEO
    Input Text           form.widgets.key_name           Olaf Organiser
    Input Text           form.widgets.key_position       CTO
    Input Text           form.widgets.key_email          olaf@organisation.org
    Input Text           form.widgets.key_phone          0123456789

    Click Button  Save
    Page Should Contain  Item created

I add a News Item
    Open Add New Menu
    Click link           news-item
    Page Should Contain  News Item
    Input Text           form.widgets.IDublinCore.title         The News Item Title
    Choose File          form.widgets.ILeadImage.image          ${CURDIR}/logo.gif
    Input Text           form.widgets.ILeadImage.image_caption  The news Item Image

    Click Button  Save
    Page Should Contain  Item created
   
I add an Event
    Open Add New Menu
    Click link           event
    Page Should Contain  Event
    Input Text           form.widgets.IDublinCore.title  The Event Title
    Input Text           form.widgets.start_date-day     27
    Select from list     form.widgets.start_date-month   February
    Input Text           form.widgets.start_date-year    2016
    Input Text           form.widgets.start_date-hour    12
    Input Text           form.widgets.start_date-min     55
    Input Text           form.widgets.end_date-day       3
    Select from list     form.widgets.end_date-month     December
    Input Text           form.widgets.end_date-year      2026
    Input Text           form.widgets.end_date-hour      10
    Input Text           form.widgets.end_date-min       05

    Click Button  Save
    Page Should Contain  Item created

I go to the Organisation
    Click link  The Organisations Title