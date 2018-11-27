# xqa-perf [![Build Status](https://travis-ci.org/jameshnsears/xqa-perf.svg?branch=master)](https://travis-ci.org/jameshnsears/xqa-perf) 
* end to end integration tests, with Matplotlib graphs.

TODO 
- https://blog.jetbrains.com/pycharm/2018/08/pycharm-2018-2-and-pytest-fixtures/
    - pytest.mark.parametrize

## 1. Test Results
* Ubuntu 18.04
### 1.1. Dell
* Memory: 7.7 GiB
* Processor: Intel® Core™ i5-3340M CPU @ 2.70GHz × 4
* Disk: 2.5" SSD

| CPU Cores | Ingest threads | Shards | Timing statistics | XML file distribution |
| ------------- | ------------- | ------------- | ------------- |
| 4 | 1 | 1 - 4 | ![4-1_1-timing_stats](graphs/4-1_4-timing_stats.png) | ![4-1_1-file_distribution](graphs/4-1_4-file_distribution.png) |
| 4 | 1 | 1 - 4 | | |
| 4 | 2 | 1 - 4 | | |
| 4 | 4 | 1 - 4 | | |

### 1.2. MSI
* Memory: 15.6 GiB
* Processor: Intel® Core™ i7-5700HQ CPU @ 2.70GHz × 8 
* Disk: M.2 SSD

| CPU Cores | Ingest threads | Shards | Timing statistics | XML file distribution |
| ------------- | ------------- | ------------- | ------------- |
| 8 | 1 | 1 - 8 | | |
| 8 | 2 | 1 - 8 | | |
| 8 | 4 | 1 - 8 | | |
| 8 | 8 | 1 - 8 | | |
