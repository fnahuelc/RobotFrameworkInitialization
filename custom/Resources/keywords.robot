*** Settings ***
Documentation    Common keywords for suite test
Library          BuiltIn
Library          Collections
Library          Libraries.AudioDevice
Library          Libraries.SoundCheck

*** Keywords ***
Include Plots in Report
    [Tags]  AudioDevice     Device
    :FOR    ${plot}    IN    @{plots}
    \   Log     ${plot}     HTML

Correct Audio Device
    [Tags]  AudioDevice     Device
    &{device}=     Get Audio Device
    variable should exist  &{device}
    should be equal  &{device}[name]    iConnectAudio4+

Enough Record Channels
    [Tags]  AudioDevice     Device
    ${numbers_channels}=    Get Number Channels Play
    should be true     ${numbers_channels}>=1

Enough Reproduction Channels
    [Tags]  AudioDevice     Device
    ${numbers_channels}=    Get Number Channels Record
    should be true     ${numbers_channels}>=1

Dis Headphone Spl
    [Tags]  IEC     Test    SoundCheck
    &{parameters}=    Get Parameters
    log   &{parameters}[power_sum]
    @{plots}=    Get Plots
    set test variable    @{plots}
    set global variable    ${parameters}

Weighted or Corrected Power Sum Is Less Than
    [Arguments]    ${value}
    should be true  &{parameters}[power_sum]<=${value}

Power Sum Is Less Than
    [Arguments]    ${value}
    [Tags]  Corroboration   Test    Values
    should be true  &{parameters}[power_sum]<=${value}

500 Hz V Sensitivity Grather Than
    [Arguments]    ${value}
    [Tags]  Corroboration   Test    Values
    should be true  &{parameters}[curve_average_v]>=${value}

500 Hz mV Sensitivity Grather Than
    [Arguments]    ${value}
    [Tags]  Corroboration   Test    Values
    should be true  &{parameters}[curve_average_mv]>=${value}

