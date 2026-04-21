## Summary

This chapter focuses on knowledge acquisition, the most critical and difficult phase in expert system development. It begins by defining knowledge and its types (procedural, factual, heuristic), then introduces knowledge engineering as the overall process of building expert systems. The chapter details knowledge acquisition techniques—ranging from natural methods like interviews and observation to contrived techniques like card sorting and repertory grids, and modeling techniques like laddering. It also covers the role of the knowledge engineer, difficulties in knowledge acquisition, and the characteristics of good knowledge.

## 1. Knowledge Basics

## 1.1 Definitions of Knowledge
- Knowledge is processed information about a domain used for solving problems.
- Knowledge consists of facts, information, or skills obtained through experience and education.
- Knowledge is practical or theoretical understanding obtained by learning, discovery, or perceiving.

## 1.2 Types of Knowledge in Expert Systems

| Type | Description | Source |
| --- | --- | --- |
| Procedural Knowledge | Step-by-step information for performing tasks | Procedures, processes |
| Factual Knowledge | Widely shared facts from textbooks and journals | Published literature |
| Heuristic Knowledge | Experiential, individualistic, less rigorous; arises from good practice and judgment | Human experts |

## 1.3 Knowledge Hierarchy

**Data → Information → Knowledge**
- **Data:** Representation of simple components (e.g., "John works for ACTME")
- **Information:** Refined data
- **Knowledge:** Refined information used for decision-making

**Formula:** Knowledge = Facts + Rules + Control Strategy + (Sometimes) Faith

## 1.4 Features of Good Knowledge
- Complete
- Consistent
- Voluminous (sufficient coverage)
- Correct and reliable

## 2. Knowledge Engineering

**Definition:** The process of building an entire knowledge-based system from beginning to end, including design, construction, and installation.

**Components of Knowledge Engineering:**
- Knowledge acquisition (from experts, books, documents, sensors, files)
- Knowledge representation (rules, frames, etc.)
- Knowledge validation and verification
- Inferencing
- Explanation and justification capabilities
## 3. Knowledge Acquisition

**Definitions:**
- The process of obtaining knowledge from domain experts using various techniques.
- The process of transforming knowledge into a representational form usable by the expert system.
- The process of gathering knowledge to form the knowledge base.

**The Knowledge Acquisition Bottleneck:**
Knowledge acquisition is the most difficult phase in knowledge engineering and is the primary cause of expert system development failures.

## 3.1 Sources of Knowledge

| Source Type | Examples |
| --- | --- |
| Documented | Textbooks, journals, historical records, databases |
| Undocumented | Human expert knowledge (heuristic knowledge) |

Documented sources alone are insufficient for real-world problems, which require heuristic knowledge from human experts.

## 3.2 Selecting a Domain Expert

Key considerations:
- Expert must possess domain expertise and heuristic knowledge
- Must be able to distribute knowledge to the team
- Must communicate clearly and explain reasoning
- Must be willing to devote significant time and effort
## 4. The Knowledge Engineer

**Role:** Acquire knowledge from domain experts and map it into AI formalisms for computational use.

**Responsibilities:**

| Task | Description |
| --- | --- |
| Knowledge elicitation | Interview experts and create knowledge bases |
| Knowledge fusion | Combine individual knowledge bases |
| Knowledge representation | Choose representation scheme (rules, frames, etc.) |
| Coding | Encode knowledge in programming language |
| Testing and evaluation | Validate system performance |

The knowledge engineer acts as an intermediary between the domain expert and the knowledge base.

## 5. Difficulties in Knowledge Acquisition

| Difficulty | Description |
| --- | --- |
| Expert's inability to justify reasoning | Experts may not be able to explain how they know what they know |
| Unwillingness to cooperate | Expert may not devote necessary time or may resist sharing |
| Incomplete knowledge | No expert knows everything about a domain |
| Tacit knowledge | Considerable implied knowledge is difficult to articulate |
| Communication barriers | Expert may not be able to describe all that they know |

**Requirements for Knowledge Acquisition Techniques:**
- Capture tacit knowledge
- Assemble knowledge from multiple experts
- Validate gathered knowledge
- Focus on essential knowledge
- Allow non-experts to understand the knowledge
## 6. Knowledge Acquisition Techniques

Knowledge acquisition techniques (also called knowledge elicitation techniques) are classified into three main categories: natural, contrived, and modeling techniques.

## 6.1 Natural Techniques
6.1.1 Interviews
Face-to-face communication between knowledge engineer and domain expert.

| Type | Description |
| --- | --- |
| Structured | Pre-planned questionnaire; goal-oriented; deals with specific concepts |
| Unstructured | No pre-planned questions; random discussion; used when knowledge engineer has little domain knowledge |
| Semi-structured | Combination; some pre-planned questions plus random questions for clarification |
| Problem-solving | Expert solves a real problem, describing each step and its justification |

**Best Practice:** Conduct interviews away from the expert's workplace; record audio for future reference.
6.1.2 Observation- Expert activities for solving real problems are observed
- Video recording is recommended
- Knowledge engineer can ask questions after observation

6.1.3 Questionnaire- Used with other techniques (e.g., interviews)
- Useful when eliciting knowledge from multiple experts
- Question list prepared when specific information is needed

## 6.2 Contrived Techniques

Specialized techniques for capturing tacit knowledge where experts perform tasks they would not normally do in their job.
6.2.1 Concept (Card) Sorting
**Purpose:** Determine how an expert compares and orders concepts; reveals tacit knowledge about classes, relations, and properties.

**Process:**
- Domain concepts are written on cards
- Cards are spread on a table
- Expert sorts cards into clusters with common characteristics
- Expert explains the principles used for grouping
- Process repeats until nothing more to sort

6.2.2 Three-Card Method
**Purpose:** Capture tacit knowledge and how experts explain concepts.

**Process:**
- Expert selects three cards randomly
- Expert explains how two cards are similar and how they differ from the third
- Helps determine features of classes

6.2.3 Repertory Grid Technique
**Purpose:** Elicit attributes for concepts and rate concepts against those attributes using numerical scales; uses statistical analysis to group similar concepts and attributes.

**Process:**

| Stage | Activity |
| --- | --- |
| 1 | Select 6–15 concepts; select approximately same number of attributes from previously elicited knowledge |
| 2 | Expert rates each concept against each attribute using numerical scale |
| 3 | Apply cluster analysis to create focus grid; group concepts with similar scores and attributes with similar scores |
| 4 | Walk expert through results for feedback; add more concepts/attributes if needed |

**Example Domain:** Crime types (petty theft, burglary, drug-dealing, murder, mugging, rape) rated against attributes (personal/impersonal, major/petty, violent/non-violent, etc.)
6.2.4 Constrained Task
Expert performs a task with constraints; useful for focusing on essential knowledge and priorities.
6.2.5 20 Questions
**Purpose:** Fast way to gain insights into key domain aspects and properties; generates new concepts.

**Process:**
- Expert asks "yes/no" questions to the knowledge engineer
- Knowledge engineer answers randomly (no deep domain knowledge needed)
- Knowledge engineer notes questions asked

6.2.6 Commentary
Expert provides running commentary while performing a task; helps elicit valuable tacit knowledge.

## 6.3 Modeling Techniques
6.3.1 Laddering
**Purpose:** Acquire concept knowledge; finds similarities and differences between groups of things.

**Uses various trees:**
- Concept tree
- Attribute tree
- Composition tree

Process involves construction, validation, and modification of trees.

## 7. Knowledge Analysis

Knowledge analysis occurs simultaneously with knowledge acquisition. It involves identifying elements needed to build the knowledge base:

| Element | Description |
| --- | --- |
| Concepts | Things that constitute a domain; main elements of the knowledge base |
| Attributes | Qualities or features belonging to a class of concepts |
| Values | Specific qualities that differentiate a concept from others |
| Relations | Ways in which concepts are associated with one another |
## 8. Conclusion

Knowledge acquisition is the foundation of expert system development. It is a complex, iterative process requiring skilled knowledge engineers and willing, articulate domain experts. The quality of the acquired knowledge directly determines the expert system's decision-making capability. Various techniques—natural, contrived, and modeling—exist to capture both explicit and tacit knowledge. The knowledge acquisition bottleneck remains a significant challenge, making the selection of appropriate techniques and experts crucial for successful expert system development. Acquired knowledge is subsequently represented using formalisms like rules, frames, or semantic networks for use by the inference engine.