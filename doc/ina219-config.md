Specific Configuration for the INA219
=====================================

The INA219 dataprovider allows the configuration of the measurement range
and the ADC-oversampling.


Measurement Range
-----------------

Available configuration options (default value: **1**):

  - **2**: 32V, 2A with 0.49mA resolution
  - **1**: 32V, 1A with 0.25mA resolution
  - **400**: 16V, 400mA with 0.01mA resolution


ADC Oversampling
----------------

Oversampling is related to noise and conversion time. A higher oversampling
will result in less noise but with a higher conversion time.

Available configuration options (default value: **6**):

  - **0**:   9 bit,    1 sample,     84us
  - **1**:  10 bit,    1 sample,    148us
  - **2**:  11 bit,    1 sample,    276us
  - **3**:  12 bit,    1 sample,    532us
  - **4**:  12 bit,    2 samples,  1.06ms
  - **5**:  12 bit,    4 samples,  2.13ms
  - **6**:  12 bit,    8 samples,  4.26ms
  - **7**:  12 bit,   16 samples,  8.51ms
  - **8**:  12 bit,   32 samples, 17.02ms
  - **9**:  12 bit,   64 samples, 34.05ms
  - **10**: 12 bit,  128 samples, 68.10ms
