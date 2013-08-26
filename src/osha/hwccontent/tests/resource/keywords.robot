*** Keywords ***
Start browser
    Open browser  ${PLONE_URL}  browser=${BROWSER}

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

I add an Organisation
    Open Add New Menu
    Click link           css=#osha-hwccontent-organisation
    Page Should Contain  Organisation
    Input Text           form.widgets.IBasic.title       The Organisations Title
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

I see the Organisation    
    Page Should Contain  The Organisations Title