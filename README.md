# xqa-perf [![Build Status](https://travis-ci.org/jameshnsears/xqa-perf.svg?branch=master)](https://travis-ci.org/jameshnsears/xqa-perf) [![Coverage Status](https://coveralls.io/repos/github/jameshnsears/xqa-perf/badge.svg?branch=master)](https://coveralls.io/github/jameshnsears/xqa-perf?branch=master) [![sonarcloud](https://sonarcloud.io/api/project_badges/measure?project=jameshnsears_xqa-perf&metric=alert_status)](https://sonarcloud.io/dashboard?id=jameshnsears_xqa-perf) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/c10d05573ec4475da87347877a8f9d75)](https://www.codacy.com/app/jameshnsears/xqa-perf?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jameshnsears/xqa-perf&amp;utm_campaign=Badge_Grade)
* end to end integration tests, with Matplotlib graphs.

## 1. Test Results
XQA allows you to easily experiment with it's operating parameters:
* the # of BaseX engines (xqa-shards).
* the # of ingest clients (xqa-ingest-balancer's pool_size).
* how long each ingest client waits for a xqa-shard size response  (xqa-ingest-balancer's insert_thread_wait & insert_thread_secondary_wait)

This ability to experiment is important as it let's you tune XQA to match your requirements.

In general though, the "best" overall scalability & performance is achieved when the # of BaseX engines and ingest client's is less than the maximum # of host CPU cores. 

By reviewing the graphs below, from a worst case ingest using a single BaseX engine, we can achieve somewhere between a 250% to 400% improvement in performance by using XQA.

### 1.1. Test Data
* Each test run used all the .xml files from [xqa-test-data](https://github.com/jameshnsears/xqa-test-data).

## 2. Test # 1 - Dell Laptop
* Ubuntu 18.04
* Memory: 7.7 GiB
* Processor: Intel® Core™ i5-3340M CPU @ 2.70GHz × 4
* Disk: 2.5" SSD

Ingest thread(s) | Shard(s) | Timing statistics | XML file distribution |
| ------------- | ------------- | ------------- | ------------- |
| 1 | 1 | ![4-1-timing_stats](graphs/4-1-timing_stats.png) | ![4-1-file_distribution](graphs/4-1-file_distribution.png) |
| 2 | 1 - 4 | ![4-2-timing_stats](graphs/4-2-timing_stats.png) | ![4-2-file_distribution](graphs/4-2-file_distribution.png) |
| 4 | 1 - 4 | ![4-4-timing_stats](graphs/4-4-timing_stats.png) | ![4-4-file_distribution](graphs/4-4-file_distribution.png) |

## 3. Test # 2 - MSI Laptop
* Ubuntu 18.04
* Memory: 15.6 GiB
* Processor: Intel® Core™ i7-5700HQ CPU @ 2.70GHz × 8 
* Disk: M.2 SSD

Ingest thread(s) | Shard(s) | Timing statistics | XML file distribution |
| ------------- | ------------- | ------------- | ------------- |
| 1 | 1 | ![8-1-timing_stats](graphs/8-1-timing_stats.png) | ![8-1-file_distribution](graphs/8-1-file_distribution.png) |
| 2 | 1 - 8 | ![8-2-timing_stats](graphs/8-2-timing_stats.png) | ![8-2-file_distribution](graphs/8-2-file_distribution.png) |
| 4 | 1 - 8 | ![8-4-timing_stats](graphs/8-4-timing_stats.png) | ![8-4-file_distribution](graphs/8-4-file_distribution.png) |
| 8 | 1 - 8 | ![8-8-timing_stats](graphs/8-8-timing_stats.png) | ![8-8-file_distribution](graphs/8-8-file_distribution.png) |
