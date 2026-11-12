# Validation

Offline (no credentials, no model calls):

```sh
python -m unittest discover -s multiagent_llm_experiment -v
python -m unittest benchmark_v3.test_runner benchmark_v3.test_validation tests.test_publication -v
python tools/verify_publication.py
python tools/reproduce.py
```

Docker integration, explicitly enabled:

```sh
docker pull python:3.12.8-alpine3.20@sha256:3b1df87fc50e7d47762aeb48673736079aa22e7c98c8851f5453dd49fc03ad1b
RUN_DOCKER_TESTS=1 python -m unittest discover -s multiagent_llm_experiment -v
python -m benchmark_v3.validate --sandbox-dir multiagent_llm_experiment --output local-validation.json
```

On Windows use the equivalent environment-variable assignment. The first command
also includes adversarial RPC regression tests; their outcome must be reported
honestly. Passing them does not remove the documented malicious-candidate integrity
limitation. Only trusted reference/fixture code is used by v3 validation.

The publication validation checks 240 unique main records, task/source hashes,
request-to-evaluation token and call reconciliation, table counts/rates, preservation
of the unresolved reserve, and imported artifact SHA-256. No API request is made.
