---
name: api-contracts
description: Design and review API contracts, including OpenAPI, YANG/RESTCONF, GraphQL, Protobuf, and event schemas. Use to specify interface behavior, identify contract drift, and assess compatibility, versioning, migration, and contract tests.
---

# API Contracts

## Scope and Operating Limits

Use design mode to propose or revise an interface contract and review mode to
compare an existing contract with its implementation or a proposed change.
For mixed requests, establish the current baseline before describing the change.

Work read-only by default and return findings or a proposal in the conversation.
Write contract artifacts only when requested. Changes to APIs, clients, generated
artifacts, tests, or other implementation require explicit authorization within
the requested scope. In both design and review, verify the target and side effects
before running checks. Obtain explicit authorization before any check involving
live calls, device operations, file generation, state changes, or other persistent
effects. If authorization is missing, describe the check as proposed.

## Discover the Contract and Its Authority

1. Read applicable repository instructions. Identify the interface technology,
   producer, consumers, visibility, and relevant supported versions. Trace the
   affected operations to requirements, decisions, data invariants, and existing
   integration conventions.
2. Locate the contract sources and how they are maintained and published. Look
   for relevant OpenAPI definitions, YANG modules and RESTCONF usage, GraphQL
   schemas, Protobuf definitions, event schemas, or code-first declarations as
   applicable. Follow imports and generation or publication configuration to
   find the maintained source for the interface and version in scope.
3. Inspect the relevant routes, handlers, serializers, validation, and error
   mappings, plus representative clients and contract tests. Cite concrete
   paths, operations, schema symbols, versions, or tests for material claims.

Identify the canonical source for each part of the contract using project
decisions and maintenance workflow. Distinguish it from generated snapshots,
client bindings, examples, and implementation evidence. Use the project's
contract format and propose changes at the maintained source, including the
upstream declarations for code-first contracts. Link to complementary canonical
sources for related rules. If sources conflict, cite both, describe the consumer
impact, and flag unresolved authority. If no canonical source can be established,
propose a format and location suited to the interface and its tooling. Avoid
creating a competing specification or hand-editing derived artifacts.

## Describe Observable Behavior

Cover the parts of the contract that matter to the affected consumers:

- Operations, resources, RPC methods, or messages, including their purpose,
  preconditions, successful outcomes, and observable side effects.
- Inputs, outputs, and metadata, including types, required and optional fields,
  nullability and omission, defaults, constraints, and validation outcomes.
  Include serialization or wire semantics where they affect interoperability.
- Error identifiers or protocol status, error payloads, and consumer handling.
  Cover malformed or invalid inputs and applicable exceptional paths such as
  conflicts, timeouts, dependency failures, and partial success.
- Authentication and authorization from the consumer's perspective, including
  required credentials or permissions and observable denial behavior.
- Where applicable, compare conformance declarations, optional features, and
  deviations with the capabilities the producer actually advertises for the
  version and environment in scope.
- Retry and idempotency guarantees where relevant, including the outcome when
  callers repeat a request after an ambiguous failure. For asynchronous flows,
  consider acknowledgement, delivery, ordering, and duplicate handling where
  they are part of the contract.

Compare the intended contract, behavior supported by inspected implementation
or observations, and consumer expectations. Describe divergences and their
impact. Mark proposed behavior as unimplemented and identify unknown or
unverified behavior and the evidence needed. Scope runtime claims to the
observed version and environment. A checked-in specification or test definition
alone establishes neither implementation nor deployed behavior.

## Compatibility and Evolution

Compare the change with the supported contract baseline. Evaluate the relevant
old and new producer-consumer combinations, including mixed versions during
rollout. Check wire and schema compatibility, generated client interfaces,
and semantic changes such as stricter validation, new enum values, changed
defaults, different errors, or changed side effects. Apply the interface
technology's evolution and compatibility rules alongside project policies.
Assess potentially additive changes against actual consumer assumptions and
decoding behavior.

Identify breaking changes and uncertain compatibility separately. For each
material change, cite the baseline, affected versions and known consumers, and
the behavior that would fail or change. Follow existing versioning and deprecation
policies. Where a break is necessary, propose an appropriate versioning or
transition mechanism, including coexistence, consumer migration order,
retirement criteria, and rollback constraints as applicable. Flag missing
consumer or release information that could change the plan.

## Contract Verification and Output

Map changed or disputed guarantees to existing or proposed contract checks.
Use the project's tooling to check producer conformance and consumer expectations
where applicable. Include the relevant success, validation, exceptional, and
version-compatibility cases. Give each important check a scenario, version pair
where relevant, and an observable pass condition. Distinguish inspected test
definitions, observed results, and proposed coverage. Schema validation alone
cannot establish behavioral compatibility.

Report the scope, baseline, and canonical references. In review, give each
material finding with expected and evidenced behavior, consumer impact, and a
proposed correction. In design, describe the proposed delta to the canonical
contract and the decisions still open. Include compatibility, migration, and
verification implications where relevant.

Keep the analysis at the interface boundary. Use `architecture` for system and
component boundaries, `data-model` for persistence and integrity, `security-design`
for threat modelling and control design, and `test-strategy` for broader verification
planning. Reference existing decision records and use `adr` when an architectural
decision needs to be recorded or revised. Report contract drift here and use
`documentation-audit` for broader documentation consistency and duplication reviews.
