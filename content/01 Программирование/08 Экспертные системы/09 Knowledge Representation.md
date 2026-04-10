## 1. Definitions of Knowledge Representation

Knowledge representation can be defined as:
- A substitute or surrogate for knowledge that helps in reasoning and decision-making
- A computational medium where reasoning can be accomplished
- A way of organizing information so that appropriate inferences can be made
- A set of ontological commitments answering "In what terms should I think about the world?"
- Fragmentary theories of intelligent reasoning, expressed through:

The representation's fundamental conception of reasoning
- The set of inferences it sanctions
- The set of inferences it recommends

**Two Perspectives:**
- **Cognitive Science:** How people store and process information
- **Artificial Intelligence:** How to store knowledge so programs can achieve human-like intelligence

## 2. Characteristics of Good Knowledge Representation

**A good KR should:**
- Represent knowledge important to the problem
- Reflect the structure of knowledge in the domain
- Capture knowledge at the appropriate level of granularity
- Support incremental, iterative development

**A good KR should NOT:**
- Be too difficult to reason about
- Require representing more knowledge than needed to solve the problem

## 3. Basics of Knowledge Representation

Two fundamental entities must be understood:

| Entity | Description |
| --- | --- |
| Facts | The truths we want to represent |
| Representation of Facts | Facts represented in a chosen format for manipulation |

**Two Levels of Structure:**
- **Knowledge Level:** Description of facts occurs here
- **Symbol Level:** Facts are represented in terms of symbols

**Mapping:**
- Forward mapping: Fact → Representation
- Backward mapping: Representation → Fact

**Example:**
- English sentence: "Dober is a dog"
- Logical representation: Dog(Dober)
- With rule: ∀x: dog(x) → hastail(x)
- Deduced: hastail(Dober)
- Backward mapping: "Dober has a tail"

*Note:* Mapping is many-to-many, not one-to-one.

## 4. Properties of Symbolic Knowledge Representation

| Property                 | Description                                         | Example                                                                         |
| ------------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------- |
| Make References Explicit | Remove ambiguity by explicitly identifying entities | "The stool (r1) was placed on the table (r2). It (r1) was broken."              |
| Referential Uniqueness   | Assign unique names to entities                     | "david-1" vs "david-2" instead of just "David"                                  |
| Semantic Uniqueness      | Each symbol has unique meaning                      | "Jackie caught a ball" (catch-object) vs "Jackie caught a cold" (catch-illness) |
| Functional Uniqueness    | Functional role is clear                            | Identifying catcher vs caught object in passive voice                           |
## 5. Properties of Good Knowledge Representation Systems

| Property                  | Description                                                       |
| ------------------------- | ----------------------------------------------------------------- |
| Representational Adequacy | Ability to represent all types of knowledge (procedural, factual) |
| Inferential Adequacy      | Ability to infer new knowledge from existing knowledge            |
| Inferential Efficiency    | Ability to focus inferential mechanisms in promising directions   |
| Acquisitional Efficiency  | Ability to acquire new information easily                         |
## 6. Categories of Knowledge Representation Schemes

| Category | Description | Examples |
| --- | --- | --- |
| Logical Schemes | Use formal logic methods to represent knowledge | Propositional logic, predicate logic |
| Network Schemes | Hierarchical structures with nodes (objects/concepts) and arcs (relations) | Semantic networks, conceptual graphs |
| Structured Schemes | Extension of networks; nodes are complex data structures with named slots | Frames, scripts |
| Procedural Schemes | Knowledge as instructions for solving problems | Production rules (IF-THEN) |

## 8. Summary of Knowledge Representation Schemes

| Scheme                | Key Features                             | Strengths                       | Weaknesses                       |
| --------------------- | ---------------------------------------- | ------------------------------- | -------------------------------- |
| Propositional Logic   | Simple propositions, connectives         | Simple, declarative             | Limited expressive power         |
| Predicate Logic       | Objects, predicates, quantifiers         | Highly expressive, formal       | Computationally complex          |
| Semantic Networks     | Nodes (concepts), arcs (relations)       | Visual, inheritance             | Ambiguity possible               |
| Frames                | Slots with values, inheritance           | Structured, default values      | Rigid structure                  |
| Scripts               | Sequences of events                      | Good for stereotyped situations | Limited to predictable scenarios |
| Conceptual Dependency | Primitive actions (ATRANS, PTRANS, etc.) | Language-independent meaning    | Complex for large domains        |
| Production Rules      | IF-THEN statements                       | Modular, easy to modify         | Can become large and complex     |