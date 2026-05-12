# Hexagonal Architecture (Ports & Adapters)

## Overview

The atomic-book project implements **strict hexagonal (ports & adapters) architecture** across all microservices. This layered design isolates domain logic from infrastructure, enabling testability and loose coupling between business logic and frameworks.

## Core Principles

- **Pure domain layer** — domain models and domain services have no Spring annotations or framework dependencies
- **Port-based abstraction** — adapters (web, persistence, messaging) depend on port interfaces, never on concrete services
- **Framework isolation** — Spring annotations appear only in config, adapters, and application services; never in domain
- **Bidirectional ports** — input ports (use-case interfaces) for inbound traffic; output ports (repository interfaces) for outbound calls
- **No framework in domain** — domain models are plain Lombok `@Value` classes; domain services are registered via `@Bean`

## Architectural Layers

### 1. Domain Layer

**Path:** `domain/`

Pure business logic with no Spring dependencies. This is the inner core—completely framework-agnostic.

#### Domain Models
- Immutable value objects using Lombok `@Value @Builder`
- Example: `User`, `RefreshToken`, `OtpCode`, `Payment`, `Reservation`
- No Spring annotations (`@Entity`, `@Component`, `@Transactional`)
- Include only domain state and validation rules

#### Domain Services
- Plain classes, registered via `@Bean` in config layer
- Common patterns: `PasswordService`, `OtpService`, `JwtService`, `PaymentProcessor`
- **Dual hashing rule** — BCrypt for low-entropy inputs (passwords, OTPs); SHA-256 for high-entropy inputs (UUID tokens)
- Can accept infrastructure dependencies (e.g., `PasswordEncoder`, `StringRedisTemplate`) in constructor, but the class itself has no `@Service` annotation

#### Domain Exceptions
- All `RuntimeException` subclasses
- Located in `domain/exception/`
- Example: `UserNotFoundException`, `InvalidCredentialsException`, `EmailAlreadyExistsException`
- Used by domain services and application services for typed error handling

### 2. Application Layer

**Path:** `application/`

Contains use cases (business operations) and ports (abstractions for inbound and outbound calls).

#### Input Ports (Use-Case Interfaces)
- **Path:** `application/port/in/`
- Define inbound operations
- Example: `Register`, `Login`, `TokenRefresh`, `SendOtp`, `CapturePayment`
- Controllers implement these interfaces via concrete application services
- DTOs live in `application/port/in/dto/`
  - Requests: mutable Lombok `@Data` beans for Jackson 3.x deserialization
  - Responses: immutable records or `final` classes (canonical constructors)

#### Output Ports (Repository Interfaces)
- **Path:** `application/port/out/`
- Define outbound abstractions for persistence, external services, or caches
- Example: `UserRepository`, `RefreshTokenRepository`, `OtpRepository` (Redis interface), `PaymentGateway`
- Shape follows the adapter's technology:
  - DB repositories: `save(entity)`, `findById(id)`, `findByXxx(xxx)`
  - Redis repositories: `save(key, value, ttl)`, `findByKey(key)`, `exists(key)`
  - External gateways: `authorize(PaymentRequest)`, `capture(transactionId)`

#### Application Services (Use-Case Implementations)
- **Path:** `application/service/`
- Implement input port interfaces
- Annotated with `@Service` and constructor-injected with port/out interfaces only
- Contain orchestration logic:
  - Call domain services for pure logic
  - Call output port interfaces for persistence or external calls
  - Throw domain exceptions for error cases
- **No framework logic** — no `@Transactional`, `@Retryable`, `@Scheduled` (these belong in config or adapters)
- Example: `RegisterService` implements `Register`, calls `UserRepository`, `PasswordService`
- **Helper services** — internal application collaborators that don't implement port/in interfaces are acceptable within the `application/` package (e.g., `RefreshTokenService`, `PaymentWriter`)

#### Transactional Boundaries
- **Pattern:** Extract long-running or multi-resource operations into a sibling `@Transactional` helper service
  - Example: `PaymentWriter` is `@Transactional` and called by `CapturePaymentService` (which is not transactional)
  - Inside one transaction: domain write + outbox event write = atomic, both succeed or both roll back
  - Avoids holding DB connection open during external gateway calls
- **Self-call bypass:** Spring AOP proxies don't wrap self-calls; extract to separate bean to apply `@Transactional`, `@Retryable`, `@Scheduled`
- **Idempotency:** When integrating `idempotency-lib`, inject `IdempotencyService`, call `preCheck()` before executing and `complete()` after success

### 3. Adapter Layer

**Path:** `adapter/`

Implements ports for inbound (controllers, filters) and outbound (persistence, gateways, messaging) concerns.

#### Inbound Adapters (adapter/in/)

**Web Controller Adapter** (`adapter/in/web/`)
- Implements input port interfaces via dependency injection
- Constructor injects port/in interfaces only (e.g., `Register`, `Login`), never concrete service classes
- Methods are thin — delegate to port/in methods, wrap response in `ApiResponse<T>`
- Return domain exceptions mapped to HTTP status codes by `GlobalExceptionHandler`
- Example: `AuthController` constructor takes `(Register, Login, TokenRefresh, Logout, OtpSend, OtpVerify)`

**Exception Handler** (`GlobalExceptionHandler`)
- Maps domain exceptions to HTTP status codes
- Examples:
  - `EmailAlreadyExistsException` → 409 Conflict
  - `UserNotFoundException` → 404 Not Found
  - `InvalidCredentialsException` → 401 Unauthorized
  - `OtpRateLimitedException` → 429 Too Many Requests
- Returns `ApiResponse.error(code, message)` for all errors

**Filter Adapter** (`adapter/in/web/filter/`)
- `MdcFilter` — reads `X-Request-Id` (generates UUID fallback), `X-User-Id`, puts in MDC
- Removes keys individually in `finally` (never calls `MDC.clear()`)
- `JwtAuthenticationFilter` — validates bearer token, populates `SecurityContextHolder`

#### Outbound Adapters (adapter/out/)

**Persistence Adapter** (`adapter/out/persistence/`)
- Implements `port/out` repository interfaces
- Uses jOOQ for type-safe SQL generation
- Example: `UserJooqRepository implements UserRepository`
- Contains private mappers (`toUser(Record)`) to reconstruct domain models from jOOQ records
- All table references are unqualified; schema routing via `connection-init-sql=SET search_path TO <schema>, public`
- **No Spring annotations on repositories** — they are plain classes instantiated via `@Bean` in config, or auto-detected via `@Component`

**Cache Adapter** (`adapter/out/cache/`)
- Implements cache-shaped repository interfaces
- Example: `OtpRepository` backed by `StringRedisTemplate`
- Redis key naming: `service:{entityId}:field` prevents collisions
- Implements TTL-based operations: `save(key, value, Duration)`, `find(key)`, `exists(key)`

**Gateway Adapter** (`adapter/out/gateway/`)
- Wraps external services (Stripe, payment processor, fraud API)
- Implements `port/out` gateway interfaces
- Example: `StripeGatewayAdapter implements PaymentGateway`
- Handles circuit breaking, retry logic, webhook signature verification

**Messaging Adapter** (`adapter/out/messaging/` or `adapter/in/kafka/`)
- Kafka producer: `KafkaTemplate` for async event emission
- Kafka consumer: `@KafkaListener` for event subscription
- Event DTOs belong in `application/port/in/event/`, not in adapter package
  - Application services must not import adapter packages
  - Kafka listeners in `adapter/in/kafka/` call port/in interfaces, not services directly

### 4. Config Layer

**Path:** `config/`

Spring configuration and infrastructure beans.

#### Common Pattern
- All config classes are `@Configuration`
- Manually create beans via `@Bean` methods rather than relying on Spring Boot autoconfiguration
- Example: `FlywayConfig`, `JwtConfig`, `SecurityConfig`, `RedisConfig`
- Reason: explicit, testable, and follows the atomic-book pattern of manual control

#### Key Configs
- **`FlywayConfig`** — create `Flyway` bean pointing to `db/migration/` resources
- **`JwtConfig`** — create `NimbusJwtEncoder`, `NimbusJwtDecoder`, register `JwtService` domain service via `@Bean`
- **`SecurityConfig`** — disable CSRF, set session policy, add custom filters
- **`RedisConfig`** — create `StringRedisTemplate` bean
- **`OutboxAutoConfiguration`** — `@EnableScheduling` (must be on `@Configuration`, not on `@Scheduled` method)
- **`IdempotencyAutoConfiguration`** — `@EnableScheduling`, `@ConditionalOnProperty` for optional enablement

#### Domain Service Registration
- Domain services (no `@Service` annotation) are registered via `@Bean` in config
- Example:
  ```java
  @Bean
  PasswordService passwordService(PasswordEncoder encoder) {
    return new PasswordService(encoder);
  }
  ```
- This allows domain services to remain framework-free while still benefiting from Spring's lifecycle and dependency injection

## Data Flow Pattern

### Example: Login (identity-service)

```
HTTP POST /auth/login {email, password}
  ↓
MdcFilter
  → Sets X-Request-Id (or generates UUID), X-User-Id in MDC
  ↓
JwtAuthenticationFilter
  → Public endpoint; skips JWT validation
  ↓
AuthController.login(LoginRequest)          [REST adapter]
  → Login.login(LoginRequest)                [port/in interface]
    → LoginService.login(...)                [application service impl]
      ↓
      UserRepository.findByEmail(email)      [port/out interface]
        → UserJooqRepository.findByEmail()   [outbound adapter]
          → DSLContext.selectFrom(USERS)... [jOOQ → PostgreSQL]
      ↓
      PasswordService.matches(raw, stored)   [domain service]
        → BCrypt.checkpw() [dual hash: BCrypt]
      ↓
      JwtService.issueAccessToken(user)      [domain service]
        → NimbusJwtEncoder.encode()           [RSA sign]
      ↓
      RefreshTokenService.issue(userId)      [app helper]
        → RefreshTokenRepository.save()       [port/out interface]
          → RefreshTokenJooqRepository.save() [outbound adapter]
            → jOOQ INSERT ... RETURNING *   [single round-trip]
  ↓
ApiResponse.success(TokenResponse)           [HTTP 200]
```

## Ports & Adapters Reference

### Identity Service Example

**Input Ports (`port/in`):**
- `Register` — create user account
- `Login` — authenticate, issue tokens
- `TokenRefresh` — refresh access token
- `Logout` — blacklist refresh token
- `OtpSend` — send OTP to phone
- `OtpVerify` — verify OTP code

**Output Ports (`port/out`):**
- `UserRepository` — user persistence (DB)
- `RefreshTokenRepository` — refresh token persistence (DB)
- `OtpRepository` — OTP storage (Redis)

**Inbound Adapters:**
- `AuthController` — REST endpoints for auth operations
- `MdcFilter` — request ID and user ID propagation
- `JwtAuthenticationFilter` — validate JWT on protected routes

**Outbound Adapters:**
- `UserJooqRepository` — PostgreSQL user store
- `RefreshTokenJooqRepository` — PostgreSQL token store
- `OtpRedisRepository` — Redis OTP cache (implements `OtpRepository` interface)

### Booking Service Example (Saga Orchestrator)

**Input Ports (`port/in`):**
- `CreateBooking` — initiate booking saga
- `CancelBooking` — cancel reservation and credits

**Output Ports (`port/out`):**
- `FraudService` — gRPC fraud check
- `PromoService` — HTTP coupon reserve/commit
- `InventoryService` — HTTP slot reservation
- `LedgerService` — HTTP payment hold/capture
- `NotificationService` — HTTP send confirmation email

**Inbound Adapters:**
- `BookingController` — REST booking endpoints
- `BookingEventListener` — Kafka consumer for payment callbacks

**Outbound Adapters:**
- `GrpcFraudAdapter` — gRPC client to fraud-service
- `HttpPromoAdapter` — HTTP client to promo-service
- `HttpInventoryAdapter` — HTTP client to inventory-service
- `HttpLedgerAdapter` — HTTP client to ledger-service
- `KafkaNotificationAdapter` — Kafka producer to notification topic

## Cross-Cutting Concerns

### Transactional Outbox (Event Emission)

**Pattern:**
1. Persist domain write + outbox event in same transaction (atomic)
2. Publish event from outbox asynchronously (polling or CDC)

**Implementation** (`outbox-lib`):
```java
@Transactional
public PaymentCaptured capture(captureRequest) {
  Payment payment = paymentRepository.save(payment);  // domain write
  outboxEventRepository.save(
    OutboxEvent("payment.captured", payment.getId(), json)
  );  // atomic
  return payment;
}

// Separate component:
@Scheduled(fixedDelayString = "${outbox.polling.interval}")
void pollAndPublish() {
  // FOR UPDATE SKIP LOCKED, send via KafkaTemplate, mark published_at
}
```

**Polling:** `@Scheduled(fixedDelay...)` with `FOR UPDATE SKIP LOCKED` prevents concurrent duplicate sends.

**CDC (Debezium):** WAL-based event capture; `published_at` never written (immutable event stream).

**Adoption:**
1. Add `outbox` Maven dependency
2. Add `classpath:db/outbox` to `FlywayConfig` migration locations
3. Add `spring-kafka` dependency + producer config
4. In application service: inject `OutboxEventRepository`, call `save()` in same transaction as domain write

### Idempotent Request Handling

**Pattern (Two-Phase):**
1. `preCheck(idempotencyKey, fingerprint, ResponseType.class)` — `INSERT ON CONFLICT DO NOTHING RETURNING *`
   - Empty result = conflict exists; re-read with `FOR UPDATE` to get status
   - If `COMPLETED`, return stored response
   - If `PROCESSING`, wait (or 409 Conflict)
2. Execute business logic
3. `complete(idempotencyKey, serializedResponse)` — `UPDATE status='COMPLETED'`

**Adoption** (`idempotency-lib`):
```java
// In REST controller:
String idempotencyKey = request.header("Idempotency-Key");

// In application service:
IdempotencyService idempotency = ...; // injected
idempotency.preCheck(idempotencyKey, fingerprint, TokenResponse.class);
TokenResponse response = loginService.login(...);
idempotency.complete(idempotencyKey, response);
return response;
```

### JWT & Token Management

**Pattern (identity-service):**
- Access tokens: short-lived (15 min), signed with RSA private key
- Refresh tokens: long-lived (7 days), stored in `refresh_tokens` table as hashed values
- JWT blacklist: Redis set with key `jwt:blacklist:{userId}`, TTL = access token expiry + 5-min buffer
  - Buffer prevents race at expiry boundary (clock skew between services)
  - Check `isBlacklisted()` before accepting token on protected routes

**Keys:**
- RSA key pair: read from `jwt.rsa.private-key` / `jwt.rsa.public-key` (PKCS8/X.509 base64)
- Dev-only placeholders in `application.properties`; replace in production

### Rate Limiting (Redis Sentinel)

**Pattern:**
- Set key with TTL; existence = 429 limit exceeded
- No counters needed; simpler and more cache-friendly

**Example (inventory-service):**
```java
String key = "inventory:" + slotId + ":reserved";
Long available = redis.decrement(key);
if (available < 0) {
  redis.increment(key);  // undo
  throw new OutOfStockException();
}
```

**Gotcha — DECR on missing key:**
- Redis auto-creates at 0, then decrements to -1
- Must check `result < 0` and undo (INCR) if limit hit
- Failing to handle causes phantom miss after Redis flush

### Observability

**Structured Logging (MDC):**
- `X-Request-Id` → correlation across services
- `X-User-Id` → user context for access logs
- Individual `MDC.remove(key)` in filter's `finally` (never `MDC.clear()`)

**Micrometer Metrics:**
- Gate counters on boolean return from transactional writes (prevent overcounting on redelivery)
- Timer: start before try, stop in finally to capture failures
- `publishPercentileHistogram(true)` for Prometheus histogram quantiles

## Enforcement & Gotchas

### Hard Rules
1. **Controllers inject ports, not services** — `@Autowired Register register` not `@Autowired RegisterService`
2. **Domain has no Spring annotations** — no `@Service`, `@Component`, `@Transactional` on domain classes
3. **Domain services registered via `@Bean`** — must appear in config layer, not auto-discovered
4. **Application services don't import adapter packages** — never `import adapter.in` or `adapter.out.gateway` in an application service

### Common Violations & Fixes

**Violation:** Controller calls repository directly
```java
// Wrong:
@RestController
class BookingController {
  @Autowired BookingRepository repo;
  public void create(CreateRequest req) {
    repo.save(...);  // ❌ skips business logic
  }
}
```
**Fix:** Call port/in interface (application service)
```java
@RestController
class BookingController {
  private final CreateBooking createBooking;
  public void create(CreateRequest req) {
    createBooking.create(req);  // ✓ goes through service
  }
}
```

**Violation:** Application service injects concrete adapter class
```java
// Wrong:
@Service
class CapturePaymentService {
  @Autowired StripeGatewayAdapter stripe;  // ❌ concrete adapter
}
```
**Fix:** Inject port/out interface
```java
@Service
class CapturePaymentService {
  private final PaymentGateway gateway;  // ✓ port abstraction
}
```

**Violation:** Domain service with `@Service` annotation
```java
// Wrong:
@Service
class PasswordService {  // ❌ framework stereotype in domain
  ...
}
```
**Fix:** Plain class registered via `@Bean`
```java
// domain/service/PasswordService.java
class PasswordService {
  ...
}

// config/SecurityConfig.java
@Configuration
class SecurityConfig {
  @Bean
  PasswordService passwordService(PasswordEncoder encoder) {
    return new PasswordService(encoder);  // ✓
  }
}
```

**Violation:** Self-call bypasses AOP (e.g., `@Transactional`)
```java
// Wrong:
@Service
class PaymentService {
  @Transactional
  void publish() { ... }
  
  void process() {
    this.publish();  // ❌ self-call, AOP proxy skipped
  }
}
```
**Fix:** Extract to sibling service
```java
// application/service/PaymentService.java
@Service
class PaymentService {
  @Autowired PaymentWriter writer;
  void process() {
    writer.publish();  // ✓ calls proxy
  }
}

// application/service/PaymentWriter.java
@Service
class PaymentWriter {
  @Transactional
  void publish() { ... }  // ✓ AOP proxy wraps this
}
```

## Testing

### Integration Test Pattern

Use `BaseIntegrationTest` with Testcontainers:
```java
class AuthControllerIntegrationTest extends BaseIntegrationTest {
  @Autowired WebTestClient client;
  @Autowired AuthController controller;
  
  @Test
  void testLogin() {
    client.post().uri("/api/auth/login")
      .bodyValue(new LoginRequest(...))
      .exchange()
      .expectStatus().isOk()
      .expectBody(ApiResponse.class)
      .jsonPath("$.data.accessToken").exists();
  }
}
```

### Library Test Pattern

For `outbox-lib` or `idempotency-lib`, test without Spring:
```java
class OutboxLibTest {
  static PostgreSQLContainer postgres = new PostgreSQLContainer<>(...);
  DSLContext dsl;
  
  @BeforeAll
  static void start() {
    postgres.start();
  }
  
  @BeforeEach
  void setup() {
    // Manual Flyway + jOOQ setup (no Spring)
    dsl = DSL.using(/* connection from postgres */);
  }
}
```

## Schema Design Patterns

**Nullable Unique Column:**
```sql
CREATE UNIQUE INDEX users_phone_key ON users(phone) WHERE phone IS NOT NULL;
```

**Token Hash Storage:**
```sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  token_hash VARCHAR(255) NOT NULL UNIQUE,  -- store hash, not raw token
  expires_at TIMESTAMPTZ NOT NULL,
  revoked BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Outbox Table:**
```sql
CREATE TABLE outbox_events (
  id UUID PRIMARY KEY,
  event_type VARCHAR(255) NOT NULL,
  aggregate_id UUID NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ  -- NULL until published
);

CREATE INDEX outbox_published_idx ON outbox_events(published_at) 
  WHERE published_at IS NULL;
```

## Persistence Technology

- **SQL:** PostgreSQL with per-service schemas (e.g., `identity` schema for identity-service)
- **ORM:** jOOQ (type-safe DSL, generated classes)
- **Migrations:** Flyway (manual versioning, one `Flyway` bean per schema)
- **Cache:** Redis (OTP codes, refresh token blacklist, inventory slots)
- **Messaging:** Kafka (inter-service events, outbox polling)
- **Search:** Elasticsearch (audit logs, business events)

## Architecture Enforcement Checklist

- [ ] Domain models: pure Lombok `@Value` classes, no Spring annotations
- [ ] Domain services: plain classes, registered via `@Bean` in config
- [ ] Application services: implement `port/in` interfaces, inject `port/out` interfaces
- [ ] Controllers: inject `port/in` interfaces only
- [ ] Exception handler: maps domain exceptions to HTTP status codes
- [ ] Repositories: implement `port/out` interfaces
- [ ] No `@Service` or `@Component` on domain or domain service classes
- [ ] No imports of `adapter` packages from `application` layer
- [ ] `@Transactional`/`@Scheduled` extracted to separate `@Service` beans to avoid self-call bypass
- [ ] Outbox write atomic with domain write in same `@Transactional` method
- [ ] Idempotency: `preCheck()` → execute → `complete()` pattern used
- [ ] Kafka events: DTOs in `application/port/in/event/`, listeners call port/in interfaces
