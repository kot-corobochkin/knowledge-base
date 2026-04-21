## 2. The Evolution of AI Usage: From Chat to Agents
- Early AI usage was simple: chatting with models like ChatGPT.
- Now, the standard is **agentic development**—agents that can access context, execute commands, and work autonomously.
- However, many developers still only use chat interfaces, which is increasingly seen as a gap.
- The author uses a **mix of 3–4 agents** regularly, and occasionally experiments with new ones.

## 3. AI and the Future of Programming Knowledge
- There is a widespread belief that AI will make foundational knowledge (algorithms, data structures) obsolete.
- The author strongly **disagrees**, citing the **"curse of knowledge"**: once you have internalized certain skills, you cannot imagine thinking without them.
- The **ability to model systems, understand trade-offs, and reason about architecture** remains essential. AI does not make a weak programmer strong—it amplifies the strong.
- Many people who claim algorithms are useless fall into two camps: those who never understood them, and those who are so proficient they no longer notice how deeply they rely on them.

## 4. Key Observations from Real-World AI Use

**AI solves symptoms, not causes:**
- AI often applies quick fixes (casting, workarounds) without addressing root problems.
- Without careful direction, it generates **technical debt at an alarming rate**.

**AI struggles with abstraction and generalization:**
- It excels at **copying patterns** (e.g., writing tests by analogy) but **never proactively suggests** refactoring or architectural improvements.
- It does not naturally see duplication or opportunities for consolidation.

**AI’s blind spots:**
- It often writes tests for irrelevant details (e.g., testing generated HTML in backend integration tests) despite clear existing examples.
- It tends to repeat code (e.g., fetching the same data multiple times) instead of extracting reusable variables.

## 5. Practical Patterns for Effective AI-Assisted Development

**Model first, code second:**
- Always define **data models and types** before generating code. Without types, AI produces inconsistent, messy structures.
- Types and schemas serve as a **contract** that keeps AI-generated code aligned.

**Barriers of abstraction:**
- Design components with **clear, minimal interfaces** (e.g., a React component that only exposes onChange and value).
- Code that is **highly isolated** can be entirely AI-generated and treated as a **black box**—easy to regenerate, easy to maintain.
- The author calls this approach **"vibe coding" for the right things**: components that are self-contained and have narrow integration points are ideal for full AI generation.

**Balancing discipline and delegation:**
- The core of the application—the **skeleton, integration logic, and architecture**—must be **designed by a human**.
- Surrounding utilities, UI components, and repetitive infrastructure can be safely generated.
- Over‑engineering with excessive rules (skills, long instruction files) creates **bureaucracy that confuses AI and degrades outcomes**.

## 6. The Role of Skills and Documentation
- **Skills** (reusable instructions for AI) and **AGENTS.md** files are useful but must be kept **minimal and stable**.
- If rules become too numerous or contradictory, they create **legacy constraints** that make AI less effective.
- The author’s own AGENTS.md is around **100 lines**—mostly project setup commands and fundamental conventions, not detailed coding rules.
- Skills should be added **only when a problem occurs repeatedly**, not preemptively.

**Author:** Кирилл Мокевнин (Kirill Mokevnin)
**Title:** Что я понял после года разработки с помощью ИИ агентов (What I Learned After a Year of Developing with AI Agents)
**Source:** Organized Programming podcast / YouTube
**Link:** https://www.youtube.com/watch?v=Au8ioLEJDOU
**Publication Date:** March 15, 2026