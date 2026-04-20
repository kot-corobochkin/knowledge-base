## 1. The NoSQL Revolution: What Remains
- The NoSQL hype has largely subsided. **SQL has won**—nearly all modern databases now support SQL or a SQL-like language.
- **MongoDB** and **Redis** are the only major NoSQL databases that still lack full SQL support.
- **Cassandra** is now actively discussing adding full SQL syntax, including joins and query optimizers.
- The author (Konstantin) predicted this trend in 2018: that SQL would return and NoSQL databases would eventually adopt it.

## 2. Why SQL Prevailed
- NoSQL databases often repeated the same mistakes SQL databases had already made (lack of standards, vendor lock-in, poor expressiveness).
- **Abstraction leakage** is a key problem: NoSQL languages often expose implementation details (indexes, replication, consistency) that should be hidden.
- Developers want **familiar, consistent, and ACID-compliant** databases. Most are not interested in new languages or eventual consistency models.
- Even Cassandra’s “insert/update/delete” operations are actually append-only mutations—this confuses developers who expect standard behavior.
[[03 Новые подходы в базах данных]]