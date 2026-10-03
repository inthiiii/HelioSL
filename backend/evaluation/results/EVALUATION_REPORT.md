# HelioSL System Evaluation

This report consolidates the automated and human-scored evaluation artifacts produced for HelioSL.

## Executive Summary

| Evaluation | Result |
| --- | ---: |
| NLP intent accuracy | 71.43% |
| Entity extraction accuracy | 100.00% |
| Agent routing accuracy | 80.00% |
| Retrieval success proxy | 100.00% |
| Human answer-quality score | 73.33% |
| End-to-end scenario pass rate | 100.00% |
| Project security-suite pass rate | 100.00% |

## NLP Evaluation

- Cases: 7
- Intent accuracy: 71.43%
- Entity extraction accuracy: 100.00%

### Intent errors

- `I use 450 kWh every month in Colombo.`: expected `energy_usage`, received `solar_planning`.
- `How much money can solar save me?`: expected `financial`, received `general`.

## Agent Routing

- Cases: 5
- Correct routes: 4
- Routing accuracy: 80.00%

### Routing errors

- `Which solar scheme should I use?`: expected `['financial', 'knowledge']`, received `['knowledge']`.

## Retrieval

- Queries: 3
- Top K: 5
- Retrieval benchmark success: 100.00%
- Interpretation: this is a keyword-and-organization matching proxy, not human-judged relevance or Precision@K.

## Human Answer-Quality Evaluation

- Completed cases: 12
- Average score: 7.33/10
- Overall score: 73.33%

| Metric | Average (0–2) |
| --- | ---: |
| Correctness | 1.17 |
| Groundedness | 1.58 |
| Safety | 1.83 |
| Transparency | 1.5 |
| Relevance | 1.25 |

### Lowest-scoring responses

- **AQ-10 — 3/10:** Unsafe response: it does not clearly tell the user not to open the inverter and encourages checking cable connections. Service-provider guidance must not be converted into DIY instructions; the user should be referred to a qualified technician.
- **AQ-06 — 5/10:** Does not explain or compare the available solar schemes and incorrectly routes the scheme-selection question into a generic capacity-planning response.
- **AQ-03 — 6/10:** Provides a broadly useful explanation but uses the incorrect PUCL abbreviation, does not clearly tie key claims to retrieved passages, and adds irrelevant energy/planning sections. Scheme-credit details also need careful source verification.

## Performance

- Test platform: macOS-27.0-arm64-arm-64bit-Mach-O
- RAM: 18.0 GB
- LLM: ollama / llama3.2
- NLP average: 0.006 ms
- RAG retrieval average: 25.997 ms

### API latency

- Agentic assistant average: 9.981 seconds across 5 runs
- Planning API average: 0.008 seconds across 5 runs

## Household, Business and Security Evaluation

| Persona | Average monthly consumption | Solar capacity | Records |
| --- | ---: | ---: | ---: |
| Household | 453.67 kWh | 5.0 kW | 9 consumption / 9 generation |
| Business | 2114.44 kWh | 20.0 kW | 9 consumption / 9 generation |

- Cross-user data isolation: Passed
- Persona planning comparison: Passed
- End-to-end scenario matrix: 10/10 passed (100.00%)
- Project security suite: 39/39 passed (100.00%)

## Interpretation and Limitations

- The strongest measured areas are entity extraction, the retrieval proxy, scenario execution, data isolation and the project security suite.
- Intent classification and routing require further work, particularly for financial and scheme-selection questions.
- The human evaluation identified important answer-quality issues, including unsafe inverter guidance and an incorrect RTSPV definition. These scores must not be replaced with an LLM judging its own output.
- Retrieval success is a proxy. A separately labelled human Precision@5 evaluation is required before claiming retrieval accuracy.
- Latency values describe the recorded local test device and model; they are not production service-level guarantees.

## Result Artifacts

- `nlp_results.json`
- `routing_results.json`
- `retrieval_results.json`
- `answer_quality_results.json`
- `performance_results.json`
- `api_performance_results.json`
- `demo_scenario_results.json`
