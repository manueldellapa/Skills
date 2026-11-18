---
name: data-model
description: Design and review repository-aware data models, database schemas, integrity constraints, and safe schema evolution. Use for entity relationships, identifiers, indexes, transactions, migration planning, backfills, compatibility analysis, and breaking schema changes.
---

# Data Model Design

Design, analyze, and review data models based on actual
repository evidence, requirements, and architectural decisions.

Preserve data integrity, schema compatibility, and migration safety.

Distinguish conceptual models, proposed designs, and implemented
database schemas.

Do not implement schema changes or execute data migrations.

## Operating Principles

- Follow applicable AGENTS.md and CLAUDE.md instructions.
- Inspect relevant repository evidence before proposing data models.
- Respect canonical requirements, existing schemas, migrations,
  architectural decisions, and established database conventions.
- Distinguish verified facts, assumptions, proposed changes,
  and unknown or uninspected behavior.
- Treat application models, migration history, and database
  constraints as evidence, not as interchangeable sources of truth.
- Identify data ownership, relationships, identifiers, lifecycle
  rules, and integrity invariants.
- Evaluate database-level and application-level constraints
  according to their actual enforcement guarantees.
- Consider compatibility, transaction boundaries, concurrency,
  migration sequencing, backfills, and rollback feasibility.
- Prefer incremental schema evolution over unnecessary redesign.
- Evaluate indexes and optimizations against demonstrated
  requirements, access patterns, and available evidence.
- Reuse existing conventions and authoritative documentation.
- Do not invent entities, constraints, migrations, or database behavior.
- Do not present proposed schema changes as already implemented.
- Operate read-only by default, including diagnostic commands
  that may create persistent side effects.
- Do not modify application models, schemas, migration files,
  database contents, or repository documentation without
  explicit authorization.
- Never execute production data migrations or destructive
  database operations as part of data-model analysis.

## Repository Discovery

Establish the existing data model and its authoritative sources
before evaluating or proposing schema changes.

1. Read applicable repository and agent instructions.
2. Identify the technology stack, database engines, ORM,
   migration tooling, and supported versions.
3. Locate canonical requirements, architecture documentation,
   ADRs, and existing data model specifications.
4. Inspect relevant application models, entity definitions,
   relationships, and persistence boundaries.
5. Examine migration history, schema definitions, constraints,
   indexes, and database configuration.
6. Review relevant queries, services, transactions, tests,
   and integration contracts.
7. Identify deployment constraints, migration procedures,
   and operational requirements when relevant.

Explore incrementally, following the entities and dependencies
relevant to the requested task.

Avoid exhaustive repository scans when focused inspection
is sufficient.

## Evidence and Source Authority

Distinguish the different sources describing the data model:

- Requirements define expected business behavior and invariants.
- Approved decisions establish architectural constraints.
- Application models describe intended application-level mappings.
- Migration files describe recorded schema evolution.
- Database definitions and catalog inspection provide evidence
  of the schema in the inspected database environment.
- Tests provide evidence of expected or verified behavior.
- Operational documentation describes deployment and
  migration procedures.

Do not assume these sources are synchronized.

A model declaration does not prove that its corresponding
database constraint has been applied.

A migration file does not prove that the migration has been
executed in a particular environment.

A database schema observed in one environment does not
establish the state of other environments.

When sources conflict, report the discrepancy and identify
the evidence required to resolve it.

Distinguish verified observations from assumptions,
interpretations, and proposed changes.

Do not claim that a constraint, index, or migration is absent
without inspecting the relevant sources sufficiently.

If direct database inspection is unavailable, state the
limitation and avoid inferring the deployed schema.

Use read-only inspection methods and respect configured
access permissions.

Do not require database access when repository evidence
is sufficient for the requested analysis.

Reference concrete repository paths, migration identifiers,
and inspected schema evidence where available.

Reuse existing authoritative documentation rather than
creating duplicate schema specifications.

## Current-State Data Model Analysis

Describe the existing data model before evaluating defects
or proposing structural changes.

Distinguish the following levels when relevant:

- Conceptual model: business entities, relationships,
  ownership, and domain invariants.
- Logical model: attributes, identifiers, cardinalities,
  optionality, and integrity rules.
- Physical schema: tables, columns, data types, indexes,
  constraints, and database-specific implementation.

Do not assume the conceptual, logical, and physical models
are identical or fully documented.

Examine relevant aspects of the existing model:

- Entities, attributes, and their responsibilities.
- Primary keys, natural keys, surrogate keys, and
  other identifiers.
- Relationships, cardinalities, and optionality.
- Foreign keys and referential integrity.
- Uniqueness, nullability, check constraints,
  and domain invariants.
- Data types, precision, defaults, and value semantics.
- Indexes and documented query access patterns.
- Data ownership, lifecycle, retention, and deletion rules.
- Transaction boundaries, consistency requirements,
  and concurrency controls.
- Shared or tenant-specific data isolation when applicable.
- Dependencies involving APIs, queries, reports,
  integrations, and downstream consumers.

Consider both database-enforced constraints and
application-enforced rules.

Identify where invariants are enforced and whether the
available evidence supports their expected guarantees.

Do not assume application-level validation provides
the same guarantees as database constraints.

Evaluate concurrency-sensitive invariants against
the actual transaction and isolation mechanisms.

Do not infer transaction safety solely from the
presence of validation logic.

Distinguish structural problems from documentation gaps,
unverified assumptions, and risks associated with
proposed changes.

Do not present an unimplemented design risk as an
existing database defect.

Reference relevant models, migrations, schema definitions,
queries, and tests when reporting findings.

Limit conclusions to the inspected evidence and
explicitly identify material uncertainties.

Avoid recommending normalization, denormalization,
indexes, or schema redesign without a demonstrated
requirement or evidence-backed problem.

## Data Model Design

Design data models from verified requirements, existing
repository conventions, and applicable architectural decisions.

Before proposing a model or schema change:

1. Identify the business problem and desired outcome.
2. Reference relevant requirements and acceptance criteria.
3. Establish the existing entities, relationships, and constraints.
4. Identify applicable ADRs and data ownership boundaries.
5. Define the invariants the proposed model must preserve.
6. Determine affected applications, integrations, and consumers.
7. Evaluate whether existing structures can satisfy the requirement.

Describe the proposed conceptual and logical model before
introducing database-specific implementation details.

Define relevant aspects of the proposed model:

- Entities, attributes, responsibilities, and ownership.
- Relationships, cardinalities, and optionality.
- Identifiers, primary keys, and uniqueness requirements.
- Referential integrity and deletion behavior.
- Nullability, defaults, data types, and value semantics.
- Business invariants and their enforcement mechanisms.
- Transaction boundaries and concurrency requirements.
- Data lifecycle, retention, and historical consistency.
- Authorization and tenant isolation where applicable.
- Expected query patterns and justified indexing needs.

Prefer existing identifiers, naming conventions, data types,
and modeling patterns when they remain appropriate.

Choose database-level constraints when strong integrity
guarantees are required and supported by the database.

Use application-level validation for business rules that
cannot be adequately expressed as database constraints.

Explain the limitations of each enforcement mechanism,
especially under concurrent operations.

Account for database-specific semantics when relevant,
including NULL handling, collation, precision,
referential actions, and transaction isolation.

Do not assume ORM behavior is identical across supported
database engines or versions.

Avoid introducing redundant entities, relationships,
indexes, or abstractions without demonstrated value.

Consider meaningful alternatives when the design introduces
significant complexity, compatibility risks, or trade-offs.

Explain why the preferred design satisfies the requirements
with acceptable integrity and maintenance costs.

Distinguish the proposed logical model from its physical
schema representation.

Identify schema changes, affected consumers, and compatibility
implications without implementing the proposal.

Flag significant changes to data ownership, consistency,
or persistence strategy for architectural decision review.

Do not create or supersede ADRs automatically.

Do not modify application models, migration files,
database schemas, or production data during design.

## Schema Evolution and Migration Safety

Evaluate schema evolution as a controlled transition from
the verified current state to the proposed target model.

Do not assume that a structurally valid target schema
can be deployed safely in a single migration.

For each significant schema change:

1. Identify affected tables, columns, constraints,
   relationships, indexes, and consumers.
2. Determine existing data conditions and invariants.
3. Classify compatibility and potential breaking changes.
4. Identify migration prerequisites and dependencies.
5. Evaluate schema migration, data migration, and
   backfill requirements separately.
6. Assess transaction boundaries, locking, concurrency,
   and deployment risks.
7. Define a safe migration sequence when necessary.
8. Evaluate rollback feasibility and recovery options.
9. Specify verification requirements and unresolved risks.

### Breaking Changes and Compatibility

Identify changes that may invalidate existing data,
queries, application behavior, or integration contracts.

Consider relevant cases such as:

- Removing or renaming tables, columns, or identifiers.
- Changing data types, precision, or value semantics.
- Introducing NOT NULL, UNIQUE, CHECK, or foreign key
  constraints on existing data.
- Changing referential actions or deletion behavior.
- Modifying identifiers or relationship cardinalities.
- Changing defaults or application-visible semantics.
- Altering data ownership or tenant isolation rules.

Distinguish backward compatibility, forward compatibility,
and compatibility during mixed-version deployments.

Identify consumers that may depend on the existing schema,
including older application versions, background workers,
reports, integrations, and external processes.

Do not assume all consumers are deployed atomically.

### Incremental Migration Strategy

Prefer incremental evolution when a direct migration
would introduce significant compatibility or data risks.

Consider an expand-migrate-contract approach when appropriate:

1. Expand the schema while preserving existing consumers.
2. Introduce compatible application behavior.
3. Migrate or backfill existing data when required.
4. Verify data integrity and consumer compatibility.
5. Remove obsolete structures only after dependencies
   have been addressed and verified.

Do not prescribe multiple deployment phases when a
single safe change is sufficient.

Separate schema changes from data transformations
when doing so improves safety and verifiability.

Evaluate idempotency, retry behavior, batching,
and resumability for substantial backfills.

Identify the authoritative data source and reconciliation
requirements during transitional states.

Do not assume that dual writes or temporary synchronization
are necessary without a demonstrated requirement.

### Operational Risks and Rollback

Evaluate relevant database-specific behavior, including:

- DDL transactional guarantees and implicit commits.
- Table locks and potential service interruption.
- Index creation and constraint validation behavior.
- Migration duration and resource consumption.
- Concurrent reads and writes during data transformation.
- Database version and migration-tool compatibility.
- Replication, backup, and recovery constraints.

Do not assume a migration is reversible merely because
the migration framework provides a rollback command.

Distinguish schema rollback, application rollback,
and restoration of transformed or deleted data.

Identify irreversible operations and potential data loss.

When reliable reversal is impossible, describe recovery
prerequisites and operational limitations.

Never claim zero downtime or safe rollback without
sufficient evidence.

Do not execute migrations, backfills, schema alterations,
or destructive operations during design and review.

Report migration sequencing, risks, required approvals,
and verification steps without performing the changes.

## Data Integrity and Verification

Evaluate whether the existing or proposed data model
preserves its required invariants under realistic
application and database behavior.

Identify relevant integrity guarantees:

- Entity identity and primary key uniqueness.
- Referential integrity and relationship consistency.
- Required values, uniqueness, and domain constraints.
- Cross-entity and application-level business invariants.
- Transaction atomicity and consistency boundaries.
- Concurrent operations and isolation behavior.
- Data ownership and tenant isolation.
- Historical consistency and lifecycle transitions.

For each significant invariant, determine:

1. The requirement or decision establishing the rule.
2. The application or database mechanism enforcing it.
3. The evidence supporting its actual enforcement.
4. Potential failure scenarios and concurrency risks.
5. The verification needed to establish confidence.

Distinguish declared constraints from verified database
constraints and observed behavior.

Do not assume that validation performed before a database
write prevents concurrent integrity violations.

Account for transaction isolation, locking, and uniqueness
guarantees when evaluating race conditions.

### Verification Approach

Define focused verification appropriate to the proposed
change and its demonstrated risks.

Consider when relevant:

- Model and migration consistency checks.
- Database catalog inspection and constraint verification.
- Tests for valid and invalid data transitions.
- Referential integrity and deletion behavior tests.
- Concurrent writes and transaction isolation tests.
- Migration testing against representative existing data.
- Backfill correctness, completeness, and repeatability.
- Compatibility tests across supported application versions.
- Rollback and recovery procedure validation.

Distinguish planned checks from checks actually executed.

Do not claim tests passed or constraints were verified
without execution evidence.

Prefer existing test infrastructure and database conventions.

Assess side effects before running diagnostic commands
or tests that may create files, databases, or persistent state.

Propose migration and backfill tests as verification plans,
not as operations to execute in this workflow.

Report unverified assumptions and residual risks.

### Worked Scenario: Introducing a Uniqueness Constraint

Consider an application that allows users to belong
to multiple projects through a membership table.

A new requirement establishes that each user may have
at most one membership per project.

The proposed schema introduces a composite uniqueness
constraint on (project_id, user_id).

Verify whether both columns are non-null.

Account for database-specific NULL semantics: a composite
UNIQUE constraint may permit multiple rows containing NULL
values and therefore fail to enforce the intended invariant.

Before recommending the change:

1. Inspect existing models, migrations, and constraints.
2. Determine whether duplicate memberships already exist.
3. Identify applications and consumers that may create
   or depend on duplicate records.
4. Define how conflicting records should be reconciled
   without silently deleting or merging business data.
5. Determine how concurrent writes are controlled during
   data reconciliation and until the uniqueness constraint
   becomes effective.
6. Plan compatible application changes and a safe
   constraint introduction sequence.
7. Identify database-specific validation and locking risks.
8. Define verification and recovery requirements.

The change is potentially breaking because existing
duplicate rows may prevent constraint creation, and
previously accepted writes may start failing.

Do not assume duplicates exist without inspecting
the relevant data or available evidence.

Do not automatically delete duplicates, apply the
constraint, or execute corrective data migrations.

Present the proposed design, required checks,
compatibility implications, and unresolved decisions.

## Data Model Output

Adapt the response to the requested task and the
complexity of the inspected data model.

For data model reviews, provide:

- Scope and inspected repository evidence.
- Verified current-state model and relevant constraints.
- Identified integrity issues and evidence-backed risks.
- Findings with concrete references and impact.
- Recommended improvements and meaningful trade-offs.
- Missing evidence, uncertainties, and verification needs.

For data model design or schema evolution proposals, provide:

- Problem, objectives, and relevant requirements.
- Verified current-state context and affected entities.
- Proposed conceptual and logical model.
- Schema impact, including affected tables, columns,
  relationships, constraints, and indexes.
- Required invariants and their enforcement mechanisms.
- Considered alternatives and relevant trade-offs.
- Compatibility and breaking-change implications.
- Migration, backfill, rollback, and operational risks.
- Proposed verification approach and acceptance checks.
- Unresolved decisions and required approvals.

Include only sections justified by the requested task.

Clearly separate verified observations, assumptions,
recommendations, and unapproved design decisions.

For each significant proposed schema change, explicitly
identify its impact on existing data and consumers.

Reference concrete repository paths, migration identifiers,
requirements, and database evidence where available.

Do not invent schema definitions, migration history,
test results, or database inspection evidence.

Prioritize findings by demonstrated impact, confidence,
and relevance to the requested task.

Consolidate overlapping findings and avoid speculative
inventories of potential problems.

Prefer actionable recommendations over exhaustive
generic database guidance.

Do not duplicate existing authoritative schema
documentation or architectural decisions.

Use diagrams or structured tables only when they
materially improve understanding of the data model.

When evidence is insufficient, explain what remains
unknown and how it could be verified.

Summarize the preferred approach and justified next actions.

Do not modify source code, database schemas, migration files,
data, documentation, or repository history without
explicit authorization.
