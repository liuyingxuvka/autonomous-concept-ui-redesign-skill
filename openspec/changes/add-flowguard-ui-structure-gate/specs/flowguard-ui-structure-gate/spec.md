## ADDED Requirements

### Requirement: Conditional FlowGuard UI structure gate
The autonomous redesign skill SHALL run or explicitly skip a FlowGuard UI Flow
Structure gate after functional framing and before concept search,
image-generation, or frontend implementation.

#### Scenario: Complex redesign triggers gate
- **WHEN** the route is `concept_redesign` and the target surface has multiple
  UI states, controls, menu levels, overlays, navigation paths, or displayed
  information ownership concerns
- **THEN** the skill MUST build or review a FlowGuard UI interaction model and
  derive a UI structure contract before visual concept work starts

#### Scenario: Minor visual-only work skips gate
- **WHEN** the route is `minor_ui_fix` and the change only affects spacing,
  color, typography, copy, or icon polish with no workflow, state, hierarchy,
  or redundancy risk
- **THEN** the skill MUST record a FlowGuard skip reason and continue without
  requiring a UI interaction model

### Requirement: FlowGuard interaction model inputs and checks
When the FlowGuard gate is triggered, the skill SHALL model UI behavior as
`UI event x UI state -> Set(UI output x UI state)` using the product goals,
required actions, required states, display-element draft, and information
architecture from functional framing.

#### Scenario: Gate has enough inputs
- **WHEN** functional framing identifies user tasks, required actions,
  required states, candidate displayed information, and non-goals
- **THEN** the FlowGuard gate MUST use those inputs to define initial state,
  controls, displayed information, transitions, availability, failure/recovery
  states, terminal states, and validation boundaries

#### Scenario: Gate cannot model missing behavior
- **WHEN** required UI behavior is too vague to model without inventing product
  behavior
- **THEN** the skill MUST mark the run as blocked or partial rather than
  proceeding to visual design with an ungrounded structure

### Requirement: Model-derived UI structure contract
When the FlowGuard gate is triggered, the skill SHALL derive a UI structure
contract from the reviewed interaction model.

#### Scenario: Structure contract is produced
- **WHEN** a reviewed UI interaction model exists
- **THEN** the skill MUST derive parent/child topology, persistent global
  regions, contextual second-level regions, local third-level controls, stable
  control placement, navigation ownership, overlay hierarchy, display ownership,
  and validation boundaries

#### Scenario: Structure is not invented from style
- **WHEN** the visual direction suggests a layout that conflicts with the
  model-derived structure contract
- **THEN** the skill MUST revise or reject the visual direction instead of
  allowing style to override the modeled UI structure

### Requirement: Duplicate information and control review
When the FlowGuard gate is triggered, the skill SHALL review duplicate
displayed information and duplicate same-level controls as explicit design
obligations.

#### Scenario: Duplicate display information appears
- **WHEN** two display elements expose the same semantic information in the
  same state or region
- **THEN** the skill MUST either merge, defer, relocate, or record an
  intentional redundancy rationale such as accessibility, summary plus detail,
  persistent context, or alternate user vocabulary

#### Scenario: Duplicate same-level controls appear
- **WHEN** two controls in the same hierarchy level perform the same function
  or lead to the same state transition
- **THEN** the skill MUST either remove, merge, relocate, or justify the
  duplication before implementation starts

### Requirement: Downstream propagation of FlowGuard contract
The autonomous redesign skill SHALL propagate the FlowGuard structure contract
into every downstream phase that can otherwise drift from the model.

#### Scenario: Concept and implementation use contract
- **WHEN** the FlowGuard gate produces a structure contract
- **THEN** the concept brief, final concept evaluation package, frontend-design
  implementation brief, iterator checklist, deviation review, geometry QA, and
  final report MUST reference the model-derived hierarchy, region ownership,
  control ownership, display ownership, redundancy decisions, and skipped or
  unresolved states

#### Scenario: Later work changes behavior
- **WHEN** concept refinement, implementation, or iteration materially changes
  controls, states, displayed information, navigation, overlays, or hierarchy
- **THEN** the skill MUST return to the FlowGuard gate or record why the change
  does not invalidate the existing model-derived structure contract
