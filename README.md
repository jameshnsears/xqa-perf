# xqa-perf [![Build Status](https://travis-ci.org/jameshnsears/xqa-perf.svg?branch=master)](https://travis-ci.org/jameshnsears/xqa-perf) 
* end to end performance metrics.
* see .travis.yml for a simple end to end test - build all containers from source; then: ingest -> ingest-balancer -> shard.
* run [bin/e2e.sh](bin/e2e.sh) to build a local end to end environment (assumes bin/build.sh run and xqa-test-data cloned beforehand).

## 1. Introduction
xqa-perf is composed of two things:
* an easy to change a unit test - [test/xqa/perf_test.py](test/xqa/perf_test.py) - that reliably demonstrates the end to end performance of xqa.
* a set of bash scripts - [bin](bin) called by the unit test but that can also be used standalone to help provision / publish the containers.

### 1.1. The Unit Test
The unit test involes multiple setup and teardown of containers, each with multiple ingest-balancer threads and shards: it is a long running test that is very CPU intensive.

Throughout the test statistics are kept and, at various intervals, graphs are output into [test_results](test_results) (see below).

### 1.2. e2e.sh - standlone environment
With bin/build.sh run and xqa-test-data cloned.

~~~~
$ ./e2e.sh 

$ docker logs dev_xqa-ingest_1 | grep "FINISHED - sent: 40/40"

$ docker logs dev_xqa-ingest-balancer_1 | grep "xqa.shard.insert." | grep "<" | wc -l
40

$ docker logs dev_xqa-shard_1 | grep "insert" | wc -l
40
~~~~

## 2. Test Environment
* CentOS 7 VM, running on a SSD with 10GB of RAM.
* 4 CPU cores.
* xqa-test-data - 40 XML files, ranging in size between 829 bytes and 14 MB.
* Host + Guest OS's in an idle state.

## 3. Test Result Graphs

### 3.1. Test: 1 ingest thread; 1 to 5 shards
![Test A](test_results/1_5.png)

### 3.2. Test: 2 ingest threads; 1 to 5 shards
![Test B](test_results/2_5.png)

### 3.3. Test: 3 ingest threads; 1 to 5 shards
![Test B](test_results/3_5.png)

### 3.4. Test: 4 ingest threads; 1 to 5 shards
![Test B](test_results/4_5.png)

### 3.5. Test: 5 ingest threads; 1 to 5 shards
![Test B](test_results/5_5.png)

## 4. Usage
Assuming [requirements.txt](requirements.txt) installed; bin/build.sh run and xqa-test-data cloned.

* export PYTHONPATH=$HOME/GIT_REPOS/xqa-perf/src:$HOME/GIT_REPOS/xqa-perf/test
* cd ~/GIT_REPOS/xqa-perf
* pytest -s
