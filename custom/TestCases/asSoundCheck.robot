*** Settings ***
Library           Selenium2Library
Library           Libraries.SoundCheck
Resource          ../Resources/keywords.robot
Resource          ../Resources/variables.robot


*** Test Cases ***
AudioDevice
    [Documentation]  Check if the current state of the device meets all the requirements
    [Tags]  AudioDevice     Device
    Correct Audio Device
    Enough Record Channels
    Enough Reproduction Channels

AsSoundCheck
    [Documentation]  IEC-60268-7 Headphone Test Sequences as SoundCheck Software
    [Tags]  IEC     Test    SoundCheck
    Rec Recall Curves Free Field
    Rec Recall Curves A
    Mes Enter Test Level    ${test_level}
    Mes Enter Impedance     ${impedance}
    Sti Tone 500 Hz V
    Sti Tone 500 Hz Mw
    Sti Wav                 ${iec_pink_file}
    Acq Play And Record V
    Acq Play And Record Mv
    Acq Play And Record Simulated Program Sig
    Ana Fundamental V
    Ana Fundamental Mv
    Ana Rta Spectrum
    Pos A Wight RTA
    Pos Ff Correct Rta
    Pos Power Sum Cs
    Pos Power Sum
    Pos Curve Average V
    Pos Curve Average Mv
    Dis Headphone Spl
    [Teardown]  Include Plots in Report

ValuesInExpectedRange
    [Documentation]  Corroborate that the obtained values are within the expected
    [Tags]  Corroboration   Test    Values
    Weighted or Corrected Power Sum Is Less Than    ${max_power_sum_cs}
    Power Sum Is Less Than  ${max_power_sum}
    500 Hz V Sensitivity Grather Than   ${min_sensivity_v}
    500 Hz mV Sensitivity Grather Than  ${min_sensivity_mv}