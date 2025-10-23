# Feature Files Directory

This directory contains Gherkin feature files that define behavior specifications for the system using the Given-When-Then format.

## Purpose

Feature files serve as:
- **Living documentation** - Human-readable specifications of system behavior
- **Acceptance criteria** - Clear definitions of what "done" means for features
- **Test scenarios** - Executable specifications that can be automated
- **Communication tool** - Bridge between business requirements and technical implementation

## File Naming Convention

Use descriptive kebab-case names that reflect the feature domain:
- `authentication.feature` - Authentication and authorization flows
- `user-profile.feature` - User profile management
- `api-validation.feature` - API contract validation
- `payment-processing.feature` - Payment workflows

## Gherkin Syntax

Feature files follow the Gherkin syntax:

```gherkin
Feature: [Feature Name]
  As a [role]
  I want [feature]
  So that [benefit]

  Scenario: [Scenario Name]
    Given [precondition]
    When [action]
    Then [expected outcome]
```

## Integration with Agent Meetings

When agents discuss feature implementation in meetings:

1. **Reference existing features** - Cite specific scenarios from .feature files
2. **QA-Engineer validates** - @QA-Engineer verifies implementations satisfy all scenarios
3. **Link to outcomes** - Meeting outcomes reference which feature files are satisfied
4. **Create new features** - If specifications are missing, QA-Engineer can propose new .feature files

### Example Meeting Reference

```markdown
@QA-Engineer, please verify the proposed login endpoint implementation
satisfies all scenarios in features/authentication.feature, particularly
the "Failed login with invalid password" and "Account lockout" scenarios.
```

## Best Practices

- **One feature per file** - Keep features focused and cohesive
- **Use Background** - Define common preconditions shared across scenarios
- **Be specific** - Use concrete examples rather than abstract descriptions
- **Keep scenarios independent** - Each scenario should be runnable in isolation
- **Use tables for multiple cases** - Scenario Outlines work well for parameterized tests

## Example Structure

```
features/
├── README.md                      # This file
├── authentication.feature         # Login, logout, password reset
├── user-profile.feature          # Profile CRUD operations
├── api-validation.feature        # API contract tests
└── example-authentication.feature # Template and reference
```

## Further Reading

- [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)
- [Writing Better Gherkin](https://cucumber.io/docs/bdd/better-gherkin/)
- [Behavior-Driven Development](https://cucumber.io/docs/bdd/)
