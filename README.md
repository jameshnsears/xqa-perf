# xqa-perf [![Build Status](https://travis-ci.org/jameshnsears/xqa-perf.svg?branch=master)](https://travis-ci.org/jameshnsears/xqa-perf) 
* end to end integration tests, with Matplotlib graphs.

## 1. Test Results
* Ubuntu 18.04

### 1.1. Dell
* Memory: 7.7 GiB
* Processor: Intel® Core™ i5-3340M CPU @ 2.70GHz × 4
* Disk: 2.5" SSD#

Ingest threads | Shards | Timing statistics | XML file distribution |
| ------------- | ------------- | ------------- | ------------- |
| 1 | 1 - 4 | ![4-1-timing_stats](graphs/4-1-timing_stats.png) | ![4-1-file_distribution](graphs/4-1-file_distribution.png) |
| 2 | 1 - 4 | ![4-2-timing_stats](graphs/4-2-timing_stats.png) | ![4-2-file_distribution](graphs/4-2-file_distribution.png) |
| 4 | 1 - 4 | ![4-4-timing_stats](graphs/4-4-timing_stats.png) | ![4-4-file_distribution](graphs/4-4-file_distribution.png) |

### 1.2. MSI
* Memory: 15.6 GiB
* Processor: Intel® Core™ i7-5700HQ CPU @ 2.70GHz × 8 
* Disk: M.2 SSD

| Ingest threads | Shards | Timing statistics | XML file distribution |
| ------------- | ------------- | ------------- | ------------- |
| 1 | 1 - 8 | ![8-1-timing_stats](graphs/4-1-timing_stats.png) | ![8-1-file_distribution](graphs/4-1-file_distribution.png) |
| 2 | 1 - 8 | ![8-2-timing_stats](graphs/4-2-timing_stats.png) | ![8-2-file_distribution](graphs/4-2-file_distribution.png) |
| 4 | 1 - 8 | ![8-4-timing_stats](graphs/4-4-timing_stats.png) | ![8-4-file_distribution](graphs/4-4-file_distribution.png) |
| 8 | 1 - 8 | ![8-8-timing_stats](graphs/4-8-timing_stats.png) | ![8-8-file_distribution](graphs/4-8-file_distribution.png) |
