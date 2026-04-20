## 4. The Shift Toward Shared Memory Architectures
- **Shared Nothing** (horizontal sharding) was the dominant trend for a decade.
- However, **SSD speeds have improved dramatically**, making **Shared Memory** (single‑node, multi‑core) architectures viable again.
- For most business needs, **5,000–10,000 RPS** is sufficient—extreme scalability is only needed by a few players (telecoms, banks, government systems).
- **PostgreSQL’s main limitation** is its storage engine (MVCC with vacuum), which creates overhead on large datasets. If this were solved (e.g., via OrioleDB or similar), PostgreSQL could capture even more of the market.

## Shared Nothing (то, что было модно последние ~10–15 лет)

Идея простая: каждый сервер работает **сам по себе**.

У него:
- своя память
- свой диск
- своя часть данных
# 2. Shared Memory (возвращение старой идеи)

Здесь наоборот:

один мощный сервер.

1 сервер  
много CPU  
много RAM  
очень быстрый SSD

Все данные лежат **в одном месте**.

Плюсы:

- проще архитектура
- быстрее разработка
- меньше багов
- меньше DevOps боли