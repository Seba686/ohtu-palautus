*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  abc
    Set Password  12345678
    Set Confirm Password  12345678
    Click Button  Register
    Page Should Contain  Welcome to Ohtu Application!

Register With Too Short Username And Valid Password
    Set Username  ab
    Set Password  12345678
    Set Confirm Password  12345678
    Click Button  Register
    Page Should Contain  Minimum username length is three

Register With Valid Username And Too Short Password
    Set Username  abc
    Set Password  1
    Set Confirm Password  1
    Click Button  Register
    Page Should Contain  Minimum password length is eight

Register With Valid Username And Invalid Password
    Set Username  abc
    Set Password  abcdefgh
    Set Confirm Password  abcdefgh
    Click Button  Register
    Page Should Contain  Password must not contain only lowercase letters

Register With Nonmatching Password And Password Confirmation
    Set Username  abc
    Set Password  12345678
    Set Confirm Password  abc45678
    Click Button  Register
    Page Should Contain  Passwords do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  12345678
    Set Confirm Password  12345678
    Click Button  Register
    Page Should Contain  User with username kalle already exists

Login After Successful Registration
    Set Username  abc
    Set Password  12345678
    Set Confirm Password  12345678
    Click Button  Register
    GO To Main Page
    Click Button  Logout
    Set Username  abc
    Set Password  12345678
    Click Button  Login
    Login Should Succeed

Login After Failed Registration
    Set Username  abc
    Set Password  12345678
    Set Confirm Password  1234
    Click Button  Register
    GO To Login Page
    Set Username  abc
    Set Password  12345678
    Click Button  Login
    Login Should Fail With Message  Invalid username or password

*** Keywords ***
Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Confirm Password
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Login Should Succeed
    Main Page Should Be Open

Login Should Fail With Message
    [Arguments]  ${message}
    Login Page Should Be Open
    Page Should Contain  ${message}

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page