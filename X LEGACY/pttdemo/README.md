# Threshold Demonstration Protocol

## Authors

* Kristian Hennings, Inventors' Way ApS

## LabBench Definition Files

| LabBench | Experiment Definition File         | Protocol Definition File         |
|:--------:|------------------------------------|----------------------------------|
| 2.7.6+   | [thrdemo.expx](thrdemo.expx) | [thrdemo.prtx](thrdemo.prtx) |

## Conditions for use

**None** - can freely be used without any requirements for a citation.

## Experiment Definition File

An example of an experiment definition file (*.expx) that uses the protocol is shown below:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<experiment xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://labbench.io https://inventors-way.github.io/LabBench.Protocols/xsd/2.7.6/experiment.xsd"            
            name="Threshold Demonstration Study"
            id="thrdemo"
            protocol="thrdemo@labbench.io">
<description />
  <experimental-setup>
    <description />
    <devices>
      <daqmx id="dev">
        <stimulators>
          <ds5 name="Stimulator" transconductance="5mA_1V" />
        </stimulators>
        <amplifiers>
          <generic-amplifier name="Applied Voltage" maximal-output-voltage="10" signal="applied-voltage">
            <gains>
              <gain name="20V/1V" gain="0.05" />
            </gains>
          </generic-amplifier>
          <generic-amplifier name="Applied Current" maximal-output-voltage="10" signal="applied-current">
            <gains>
              <gain name="10mA/1V" gain="10"/>
            </gains>
          </generic-amplifier>
        </amplifiers>
      </daqmx>
    </devices>
    <device-mapping>      
      <device-assignment test-type="psychophysics-threshold-estimation" instrument-name="Button" device-id="dev" />
      <device-assignment test-type="psychophysics-threshold-estimation" instrument-name="Stimulator" device-id="dev" />
      <device-assignment test-type="psychophysics-threshold-estimation" instrument-name="SweepSampler" device-id="dev" />
    </device-mapping>
  </experimental-setup>
</experiment>
```

Template experiment definition files for each version of the protocol can be downloaded from the section [LabBench Definition Files](#labbench-definition-files).

## How to install the experiment

To install the experiment in LabBench, download the experiment definition file and run the following command:

```dos
labbench add -e thrdemo.expx
```

from the directory to which you downloaded the experiment definition file.