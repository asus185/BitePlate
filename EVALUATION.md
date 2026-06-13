# Technical Evaluation — BitePlate SRMS Web

## Pattern Selection Justification

### Singleton (OrderHistoryLog)
The Singleton pattern was the best fit for the Order History Log because the system requires a single, globally accessible log instance. Alternatives considered:
- **Static Class:** Would work but lacks lazy initialization flexibility.
- **Dependency Injection:** More testable but adds unnecessary complexity.

**Trade-offs:** Simplifies global access but introduces testing challenges (state persistence between tests) and thread safety concerns. For production, `threading.Lock()` or a database-backed solution would be necessary.

### Command Pattern (KitchenQueue)
The Command pattern addresses the kitchen queue's need for execute/undo functionality. Alternatives:
- **Simple Function Calls:** Would not support undo or command history.
- **Memento Pattern:** Could save state but would be heavier and less granular.

**Trade-offs:** Adds complexity through multiple command classes but provides excellent extensibility. Commands are decoupled from the invoker — `KitchenQueue.execute_next()` manages history after execution, preserving encapsulation.

### Strategy Pattern (PricingEngine)
The Strategy pattern enables runtime pricing strategy swapping without modifying the Bill class. Alternatives:
- **Conditional Logic (if/else):** Would violate Open/Closed Principle.
- **Template Method:** Less flexible for runtime changes.

**Trade-offs:** Requires separate classes per strategy but makes adding new pricing modes trivial.

## Coherent Pattern Flow
The three patterns work together in a single flow:
1. **Command** — Waiter confirms order → `PrepareOrderCommand` added to `KitchenQueue`
2. **Singleton** — Order logged to `OrderHistoryLog` with timestamp, table, staff, items, total
3. **Strategy** — Cashier applies pricing strategy → `PricingEngine` calculates discounted total

## Singleton Trade-offs: Testability & Thread Safety
The current Singleton is not thread-safe. Race conditions could create multiple instances in multi-threaded environments. Testability suffers because state persists between tests — requiring `clear_logs()` calls or test fixtures.

## Scaling to 50 Restaurants
If BitePlate scales to 50 locations:
1. **Singleton → Database:** In-memory Singleton replaced with PostgreSQL for persistence and multi-instance sync.
2. **Command Pattern:** Would require a message queue (e.g., RabbitMQ) for distributed kitchen stations.
3. **Observer Pattern:** Would need pub/sub (e.g., Redis Pub/Sub) for cross-instance notifications.
4. **Strategy Pattern:** Would remain unchanged as it's stateless.
5. **Config:** Credentials would move to environment variables or a secrets manager.
