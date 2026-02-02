# UK Fuel Finder API - Design

## Architecture Overview

The library follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         Public API Interface            │
│  (FuelFinderClient, convenience methods)│
└─────────────────────────────────────────┘
                  │
┌─────────────────────────────────────────┐
│         Service Layer                   │
│  (PriceService, Forecourt Service)      │
└─────────────────────────────────────────┘
                  │
┌─────────────────────────────────────────┐
│         Core Components                 │
│  (Auth, HTTP, Cache, RateLimit)         │
└─────────────────────────────────────────┘
                  │
┌─────────────────────────────────────────┐
│         External API                    │
│  (api.fuelfinder.service.gov.uk)        │
└─────────────────────────────────────────┘
```

## Component Design

### 1. Authentication Module (`auth.py`)

**Responsibility**: Handle OAuth 2.0 client credentials flow

**Classes**:
- `OAuth2Authenticator`: Manages token lifecycle

**Key Methods**:
```python
class OAuth2Authenticator:
    def __init__(self, client_id: str, client_secret: str, token_url: str)
    def get_token(self) -> str
    def refresh_token(self) -> str
    def is_token_expired(self) -> bool
```

**Token Management**:
- Store token and expiry time in memory
- Automatically refresh 60 seconds before expiry
- Thread-safe token access
- Retry logic for token endpoint failures

**Sequence Diagram**:
```
Client          Authenticator       Token Endpoint
  │                  │                     │
  │──get_token()────>│                     │
  │                  │──POST /token───────>│
  │                  │<──access_token──────│
  │                  │ (cache token)       │
  │<──token──────────│                     │
  │                  │                     │
  │──get_token()────>│                     │
  │  (cached)        │                     │
  │<──token──────────│                     │
```

### 2. HTTP Client Module (`http_client.py`)

**Responsibility**: Handle all HTTP communication with API

**Classes**:
- `HTTPClient`: Wrapper around requests library

**Key Methods**:
```python
class HTTPClient:
    def __init__(self, base_url: str, authenticator: OAuth2Authenticator, timeout: int = 30)
    def get(self, endpoint: str, params: dict = None) -> dict
    def _make_request(self, method: str, endpoint: str, **kwargs) -> dict
    def _handle_response(self, response: requests.Response) -> dict
```

**Features**:
- Automatic authentication header injection
- Response validation and parsing
- HTTP error handling
- Request/response logging
- Timeout configuration

**Error Mapping**:
- 401 → AuthenticationError (trigger token refresh)
- 404 → NotFoundError
- 429 → RateLimitError
- 5xx → ServerError
- Timeout → TimeoutError

### 3. Cache Module (`cache.py`)

**Responsibility**: Cache API responses to reduce redundant requests

**Classes**:
- `ResponseCache`: In-memory cache with TTL

**Key Methods**:
```python
class ResponseCache:
    def __init__(self)
    def get(self, key: str) -> Optional[dict]
    def set(self, key: str, value: dict, ttl: int)
    def clear(self)
    def _generate_key(self, endpoint: str, params: dict) -> str
```

**Cache Strategy**:
- Key: Hash of endpoint + sorted params
- TTL: Configurable per resource type
  - Forecourts: 3600s (1 hour)
  - Prices: 900s (15 minutes)
- Eviction: Lazy deletion on access
- Thread-safe operations

### 4. Rate Limiter Module (`rate_limiter.py`)

**Responsibility**: Enforce rate limits and implement backoff

**Classes**:
- `RateLimiter`: Track and enforce request limits

**Key Methods**:
```python
class RateLimiter:
    def __init__(self, requests_per_minute: int, daily_limit: int)
    def acquire(self) -> None
    def handle_rate_limit_error(self, retry_after: int) -> None
    def _wait_if_needed(self) -> None
```

**Features**:
- Sliding window rate limiting
- Exponential backoff on 429 errors
- Respect Retry-After header
- Per-environment limits (test vs production)

**Backoff Strategy**:
```
Attempt 1: Wait 1 second
Attempt 2: Wait 2 seconds
Attempt 3: Wait 4 seconds
Max retries: 3
```

### 5. Service Layer

#### Price Service (`services/price_service.py`)

**Responsibility**: Business logic for fuel price operations

**Key Methods**:
```python
class PriceService:
    def __init__(self, http_client: HTTPClient, cache: ResponseCache)
    def get_prices(self, fuel_type: str = None, location: dict = None, page: int = 1) -> dict
    def get_price_by_id(self, price_id: str) -> dict
    def search_prices(self, filters: dict) -> dict
```

#### Forecourt Service (`services/forecourt_service.py`)

**Responsibility**: Business logic for forecourt operations

**Key Methods**:
```python
class ForecourtsService:
    def __init__(self, http_client: HTTPClient, cache: ResponseCache)
    def get_forecourts(self, location: dict = None, page: int = 1) -> dict
    def get_forecourt_by_id(self, forecourt_id: str) -> dict
    def search_forecourts(self, filters: dict) -> dict
```

### 6. Client Interface (`client.py`)

**Responsibility**: Main entry point for library users

**Class**:
```python
class FuelFinderClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        environment: str = "production",
        cache_enabled: bool = True,
        timeout: int = 30
    )
    
    # Price methods
    def get_prices(self, **kwargs) -> dict
    def get_price(self, price_id: str) -> dict
    
    # Forecourt methods
    def get_forecourts(self, **kwargs) -> dict
    def get_forecourt(self, forecourt_id: str) -> dict
    
    # Utility methods
    def clear_cache(self) -> None
    def set_cache_ttl(self, resource_type: str, ttl: int) -> None
```

**Initialization Flow**:
```
User creates client
    │
    ├─> Load configuration
    ├─> Initialize authenticator
    ├─> Initialize HTTP client
    ├─> Initialize rate limiter
    ├─> Initialize cache
    ├─> Initialize services
    └─> Return client instance
```

## Data Models

### Configuration Model
```python
@dataclass
class Config:
    client_id: str
    client_secret: str
    environment: str
    base_url: str
    token_url: str
    timeout: int
    cache_enabled: bool
    rate_limit_rpm: int
    rate_limit_daily: int
```

### Response Models
```python
@dataclass
class Price:
    id: str
    forecourt_id: str
    fuel_type: str
    price: float
    currency: str
    updated_at: datetime

@dataclass
class Forecourt:
    id: str
    name: str
    address: dict
    operator: str
    brand: str
    amenities: list
    opening_hours: dict
    location: dict  # lat, lon
```

## Error Hierarchy

```
FuelFinderError (base)
├── AuthenticationError
│   ├── InvalidCredentialsError
│   └── TokenExpiredError
├── APIError
│   ├── NotFoundError
│   ├── RateLimitError
│   ├── ServerError
│   └── ValidationError
├── NetworkError
│   ├── TimeoutError
│   └── ConnectionError
└── ResponseParseError
```

## Configuration Management

### Environment Variables
```bash
FUEL_FINDER_CLIENT_ID=your_client_id
FUEL_FINDER_CLIENT_SECRET=your_client_secret
FUEL_FINDER_ENVIRONMENT=production  # or test
```

### Configuration File (optional)
```yaml
# fuel_finder_config.yaml
client_id: ${FUEL_FINDER_CLIENT_ID}
client_secret: ${FUEL_FINDER_CLIENT_SECRET}
environment: production
timeout: 30
cache:
  enabled: true
  ttl:
    forecourts: 3600
    prices: 900
```

## API Endpoints (Based on Documentation)

### Base URLs
- **Production**: `https://api.fuelfinder.service.gov.uk`
- **Test**: `https://test-api.fuelfinder.service.gov.uk` (assumed)

### Token Endpoint
- **URL**: `/oauth/token` (assumed based on OAuth 2.0 standards)
- **Method**: POST
- **Content-Type**: application/x-www-form-urlencoded

### Prices Endpoints
- `GET /v1/prices` - List all prices with optional filters
- `GET /v1/prices/{id}` - Get specific price by ID

**Query Parameters**:
- `fuel_type`: Filter by fuel type (unleaded, diesel, etc.)
- `latitude`, `longitude`, `radius`: Geographic filtering
- `page`, `per_page`: Pagination

### Forecourts Endpoints
- `GET /v1/forecourts` - List all forecourts with optional filters
- `GET /v1/forecourts/{id}` - Get specific forecourt by ID

**Query Parameters**:
- `latitude`, `longitude`, `radius`: Geographic filtering
- `operator`: Filter by operator
- `page`, `per_page`: Pagination

## Security Considerations

### Credential Storage
- Never hardcode credentials in source code
- Use environment variables or secure config files
- Support credential rotation without code changes

### Token Security
- Store tokens in memory only (never disk)
- Clear tokens on client destruction
- Use HTTPS for all API communication
- Validate SSL certificates

### Input Sanitization
- Validate all user inputs before API requests
- Escape special characters in query parameters
- Limit string lengths to prevent abuse
- Validate numeric ranges

## Performance Optimization

### Caching Strategy
- Cache GET requests only
- Use LRU eviction if memory limits reached
- Provide cache statistics for monitoring
- Allow cache warming for common queries

### Connection Pooling
- Reuse HTTP connections via requests.Session
- Configure connection pool size
- Set appropriate keep-alive timeouts

### Pagination Handling
- Provide iterator for automatic pagination
- Lazy loading of paginated results
- Configurable page size

## Testing Strategy

### Unit Tests
- Mock all external API calls
- Test error handling paths
- Test cache behavior
- Test rate limiting logic
- Test authentication flow

### Integration Tests
- Use test environment credentials
- Test actual API interactions
- Verify response parsing
- Test pagination
- Test rate limit handling

### Test Fixtures
- Sample API responses
- Mock token responses
- Error response examples

## Logging Strategy

### Log Levels
- **DEBUG**: Request/response details, cache hits/misses
- **INFO**: API calls, token refresh
- **WARNING**: Rate limit approaching, retries
- **ERROR**: API errors, authentication failures

### Log Format
```
[2026-02-02 18:45:15] [fuelfinder.http_client] [INFO] GET /v1/prices?fuel_type=unleaded (200) 245ms
[2026-02-02 18:45:16] [fuelfinder.cache] [DEBUG] Cache hit: prices:fuel_type=unleaded
[2026-02-02 18:45:17] [fuelfinder.auth] [INFO] Token refreshed successfully
```

### Sensitive Data Masking
- Mask client secrets: `client_secret=***`
- Mask tokens: `Bearer eyJ...` → `Bearer ***`
- Log request IDs for tracing

## Dependencies

### Core Dependencies
- `requests>=2.31.0` - HTTP client
- `python-dateutil>=2.8.0` - Date parsing

### Optional Dependencies
- `pyyaml>=6.0` - Config file support
- `httpx>=0.24.0` - Async support (future)

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `responses>=0.23.0` - HTTP mocking
- `black>=23.0.0` - Code formatting
- `mypy>=1.0.0` - Type checking

## Package Structure

```
fuelfinder/
├── __init__.py
├── client.py
├── auth.py
├── http_client.py
├── cache.py
├── rate_limiter.py
├── config.py
├── exceptions.py
├── models.py
├── services/
│   ├── __init__.py
│   ├── price_service.py
│   └── forecourt_service.py
└── utils/
    ├── __init__.py
    └── validators.py

tests/
├── unit/
│   ├── test_auth.py
│   ├── test_http_client.py
│   ├── test_cache.py
│   └── test_rate_limiter.py
├── integration/
│   ├── test_prices.py
│   └── test_forecourts.py
└── fixtures/
    └── responses.py
```

## Future Enhancements

### Phase 2 (Post-MVP)
- Async/await support with httpx
- Webhook support for price updates
- Bulk operations
- Advanced filtering and search
- GraphQL support (if API adds it)

### Phase 3
- CLI tool for quick queries
- Price change notifications
- Historical data tracking
- Analytics and reporting
- Multi-region support
