*** Settings ***

Library  Selenium2Library  timeout=10  implicit_wait=0.5
Resource  plone/app/robotframework/selenium.robot
Resource  keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote
