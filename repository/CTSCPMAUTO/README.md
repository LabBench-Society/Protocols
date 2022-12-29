# Temporal summation and Conditioned Pain Modulation (Compressor Test)

This protocol is intended as a protocol to determine the required air supply for the [Temporal summation and Conditioned Pain Modulation protocol](https://github.com/LabBench-Society/Protocols/tree/main/repository/CTSCPM) (```ctscpm@labbench.io```) and **NOT** as a protocol for actual experiments. With this protocol, you can determine if a given air supply system, such as a compressor or diving bottle, holds sufficient air for the number of consecutive sessions you plan to perform in your study.

This protocol contains the same cuff pressure algometry tests as the ```ctscpm@labbench.io``` protocol, with an additional survey test at the end of the protocol. This survey test allows you to enter the remaining air supply pressure at the end of the protocol. In this protocol, autostart is enabled. All tests will run automatically when you click start in the LabBench Start-up Wizard. 

The idea in the protocol is to run the protocol to completion until the air supply pressure falls below 200kPa, which is the minimal air supply pressure that the CPAR+ device requires to operate. It assumes that the air tank is fully pressurised to prevent unwanted noise during an experiment, and then the compressor is turned off. The air tank must hold sufficient pressure for an entire workday or a session, depending on whether the air tank can be repressurised after each session.

## Experimental setup

![](ExperimentalSetup.png)

*Figure 1: Experimental setup for testing if a compressor or similar air supply system (Device Under Test) has a sufficient air supply for an experimental protocol.*

## Protocol


## Data analysis