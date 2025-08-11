# API Endpoints Guide

## Table of Contents

1. [Overview](#overview)
2. [Security Features](#security-features)
3. [Endpoint Reference](#endpoint-reference)
4. [Usage Examples](#usage-examples)
5. [Rate Limiting](#rate-limiting)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)

## Overview

The Haive API provides secure, scalable endpoints for data processing and machine learning operations. All endpoints implement comprehensive security measures including rate limiting, input validation, and thread-safe operations.

### Base Architecture

```python
from haive.api.endpoints import MLEndpoint, DataEndpoint, BatchEndpoint
from haive.core import DataProcessor
from haive.ml import MLPipeline

# Initialize components
processor = DataProcessor()
pipeline = MLPipeline(processor)

# Create endpoints
ml_endpoint = MLEndpoint(pipeline)
data_endpoint = DataEndpoint(processor)
batch_endpoint = BatchEndpoint(ml_pipeline=pipeline, data_processor=processor)
```

## Security Features

### Built-in Protection

1. **Rate Limiting**: Configurable request limits per time window
2. **Input Validation**: Size limits and type checking
3. **Thread Safety**: Lock-based protection for concurrent requests
4. **Error Sanitization**: Safe error messages for clients

### Configuration

```python
# Rate limiting configuration
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 100  # requests per window

# Size limits
MAX_SAMPLES = 100
MAX_DATA_SIZE = 50000  # 50KB
MAX_BATCH_OPERATIONS = 50
```

## Endpoint Reference

### MLEndpoint

Machine learning prediction endpoint for model inference.

#### Request Format

```python
{
    "samples": [
        {"feature1": 1.0, "feature2": 2.0},
        {"feature1": 3.0, "feature2": 4.0}
    ]
}
```

#### Response Format

```python
{
    "success": true,
    "predictions": [0.95, 0.87],
    "confidence": [0.99, 0.95],
    "model_version": "1.0.0",
    "metadata": {
        "endpoint": "ml",
        "request_id": 123,
        "samples_count": 2
    }
}
```

#### Validation Rules

- Maximum 100 samples per request
- Each sample must be a dictionary
- Each sample limited to 10KB

### DataEndpoint

Data processing endpoint for transformations and validations.

#### Request Format

```python
{
    "data": {
        "field1": "value1",
        "field2": 42,
        "nested": {
            "subfield": "value"
        }
    }
}
```

#### Response Format

```python
{
    "success": true,
    "processed_data": {
        "field1": "VALUE1",
        "field2": 42,
        "nested": {...},
        "_processed": true,
        "_timestamp": "2025-01-11T10:30:00Z"
    },
    "metadata": {
        "endpoint": "data",
        "request_id": 456,
        "processor_stats": {
            "total_processed": 1234,
            "errors": 5
        }
    }
}
```

#### Validation Rules

- Data must be a dictionary
- Maximum size: 50KB
- No dangerous keys (starting with \__ or _)

### BatchEndpoint

Batch processing for multiple operations in a single request.

#### Request Format

```python
{
    "operations": [
        {
            "type": "predict",
            "data": {"feature1": 1.0}
        },
        {
            "type": "process",
            "data": {"field1": "value"}
        }
    ]
}
```

#### Response Format

```python
{
    "success": true,
    "results": [
        {
            "operation_index": 0,
            "success": true,
            "result": {
                "predictions": [0.95],
                "confidence": [0.99]
            }
        },
        {
            "operation_index": 1,
            "success": true,
            "result": {...}
        }
    ],
    "metadata": {
        "endpoint": "batch",
        "request_id": 789,
        "batch_id": 10,
        "operations_count": 2,
        "successful_operations": 2
    }
}
```

#### Validation Rules

- Maximum 50 operations per batch
- Each operation must have 'type' and 'data'
- Supported types: 'predict', 'process'

## Usage Examples

### Python Client Example

```python
import requests
import json

class HaiveAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def predict(self, samples):
        """Make ML predictions."""
        response = self.session.post(
            f"{self.base_url}/ml/predict",
            json={"samples": samples}
        )
        return response.json()

    def process_data(self, data):
        """Process data."""
        response = self.session.post(
            f"{self.base_url}/data/process",
            json={"data": data}
        )
        return response.json()

    def batch_operations(self, operations):
        """Execute batch operations."""
        response = self.session.post(
            f"{self.base_url}/batch",
            json={"operations": operations}
        )
        return response.json()

# Usage
client = HaiveAPIClient()

# Single prediction
result = client.predict([
    {"temperature": 25.0, "humidity": 60.0}
])
print(f"Prediction: {result['predictions'][0]}")

# Data processing
result = client.process_data({
    "user_id": "12345",
    "action": "login"
})
print(f"Processed: {result['processed_data']}")

# Batch operations
result = client.batch_operations([
    {"type": "predict", "data": {"temp": 20.0}},
    {"type": "process", "data": {"event": "click"}}
])
print(f"Batch results: {result['results']}")
```

### cURL Examples

```bash
# ML Prediction
curl -X POST http://localhost:8000/ml/predict \
  -H "Content-Type: application/json" \
  -d '{
    "samples": [
      {"feature1": 1.0, "feature2": 2.0}
    ]
  }'

# Data Processing
curl -X POST http://localhost:8000/data/process \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "test",
      "value": 42
    }
  }'

# Batch Operations
curl -X POST http://localhost:8000/batch \
  -H "Content-Type: application/json" \
  -d '{
    "operations": [
      {"type": "predict", "data": {"x": 1}},
      {"type": "process", "data": {"y": 2}}
    ]
  }'
```

### JavaScript/TypeScript Example

```typescript
interface PredictionRequest {
  samples: Array<Record<string, number>>;
}

interface ProcessRequest {
  data: Record<string, any>;
}

class HaiveAPI {
  private baseURL: string;

  constructor(baseURL = "http://localhost:8000") {
    this.baseURL = baseURL;
  }

  async predict(samples: Array<Record<string, number>>) {
    const response = await fetch(`${this.baseURL}/ml/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ samples }),
    });
    return response.json();
  }

  async processData(data: Record<string, any>) {
    const response = await fetch(`${this.baseURL}/data/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data }),
    });
    return response.json();
  }
}

// Usage
const api = new HaiveAPI();

// Make prediction
const prediction = await api.predict([{ feature1: 1.0, feature2: 2.0 }]);
console.log("Prediction:", prediction.predictions[0]);
```

## Rate Limiting

### How It Works

The API implements a token bucket algorithm:

1. Each client/IP gets a bucket with 100 tokens
2. Each request consumes 1 token
3. Tokens refill over a 60-second window
4. Requests are rejected when bucket is empty

### Handling Rate Limits

```python
# Client-side rate limit handling
import time

def make_request_with_retry(client, method, *args, max_retries=3):
    """Make request with rate limit retry logic."""
    for attempt in range(max_retries):
        try:
            result = getattr(client, method)(*args)
            if result.get('error_type') == 'RateLimitError':
                # Wait and retry
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    return None
```

### Custom Rate Limits

```python
# Configure custom rate limiter
from haive.api.endpoints import RateLimiter

# Create custom rate limiter
custom_limiter = RateLimiter(
    window=300,  # 5 minutes
    max_requests=500  # 500 requests per 5 minutes
)

# Apply to endpoint
ml_endpoint.rate_limiter = custom_limiter
```

## Error Handling

### Error Response Format

```python
{
    "success": false,
    "error": "Error message",
    "error_type": "ErrorType",
    "metadata": {
        "endpoint": "ml",
        "request_id": 123
    }
}
```

### Error Types

1. **ValidationError**: Client input validation failed
   - Safe to retry with corrected input
   - Error message contains details

2. **InternalError**: Server-side error
   - Generic message for security
   - Check server logs for details

3. **RateLimitError**: Rate limit exceeded
   - Retry after waiting
   - Check rate limit headers

### Client Error Handling

```python
def handle_api_response(response):
    """Handle API response with proper error checking."""
    if response['success']:
        return response

    error_type = response['error_type']
    error_msg = response['error']

    if error_type == 'ValidationError':
        # Log and fix input
        logger.warning(f"Validation failed: {error_msg}")
        raise ValueError(error_msg)

    elif error_type == 'RateLimitError':
        # Wait and retry
        logger.info("Rate limit hit, waiting...")
        raise RateLimitException(error_msg)

    elif error_type == 'InternalError':
        # Server error, contact support
        logger.error(f"Server error: {error_msg}")
        raise ServerException(error_msg)

    else:
        # Unknown error
        raise Exception(f"Unknown error: {error_msg}")
```

## Best Practices

### 1. Input Validation

Always validate inputs before sending:

```python
def validate_samples(samples):
    """Validate ML samples before sending."""
    if not isinstance(samples, list):
        raise ValueError("Samples must be a list")

    if len(samples) > 100:
        raise ValueError("Too many samples (max 100)")

    for i, sample in enumerate(samples):
        if not isinstance(sample, dict):
            raise ValueError(f"Sample {i} must be a dict")

        # Check size
        if len(json.dumps(sample)) > 10000:
            raise ValueError(f"Sample {i} too large")

    return True
```

### 2. Connection Pooling

Use connection pooling for better performance:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    """Create session with connection pooling and retry."""
    session = requests.Session()

    # Retry strategy
    retry = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504]
    )

    # Connection pooling
    adapter = HTTPAdapter(
        pool_connections=10,
        pool_maxsize=10,
        max_retries=retry
    )

    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session
```

### 3. Batch Optimization

Use batch endpoint for multiple operations:

```python
# Instead of multiple calls
results = []
for data in dataset:
    result = client.predict([data])
    results.append(result)

# Use batch endpoint
operations = [
    {"type": "predict", "data": data}
    for data in dataset
]
result = client.batch_operations(operations)
```

### 4. Error Recovery

Implement proper error recovery:

```python
def process_with_recovery(client, data_list):
    """Process data with error recovery."""
    results = []
    failed = []

    for data in data_list:
        try:
            result = client.process_data(data)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to process {data}: {e}")
            failed.append({
                'data': data,
                'error': str(e)
            })

    # Retry failed items
    if failed:
        logger.info(f"Retrying {len(failed)} failed items")
        # Implement retry logic

    return results, failed
```

### 5. Monitoring

Monitor API usage:

```python
class MonitoredClient(HaiveAPIClient):
    """API client with monitoring."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics = {
            'requests': 0,
            'errors': 0,
            'latency': []
        }

    def _track_request(self, method, duration, success):
        """Track request metrics."""
        self.metrics['requests'] += 1
        if not success:
            self.metrics['errors'] += 1
        self.metrics['latency'].append(duration)

    def get_metrics(self):
        """Get client metrics."""
        return {
            'total_requests': self.metrics['requests'],
            'error_rate': self.metrics['errors'] / max(1, self.metrics['requests']),
            'avg_latency': sum(self.metrics['latency']) / max(1, len(self.metrics['latency']))
        }
```

## Integration Examples

### Flask Integration

```python
from flask import Flask, request, jsonify
from haive.api.endpoints import MLEndpoint

app = Flask(__name__)
ml_endpoint = MLEndpoint(pipeline)

@app.route('/ml/predict', methods=['POST'])
def predict():
    # Get client identifier for rate limiting
    client_id = request.remote_addr

    # Check rate limit
    if not rate_limiter.is_allowed(client_id):
        return jsonify({
            'success': False,
            'error': 'Rate limit exceeded',
            'error_type': 'RateLimitError'
        }), 429

    # Process request
    result = ml_endpoint.handle_request(request.json)
    status_code = 200 if result['success'] else 400

    return jsonify(result), status_code
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from haive.api.endpoints import DataEndpoint

app = FastAPI()
data_endpoint = DataEndpoint(processor)

class DataRequest(BaseModel):
    data: dict

@app.post('/data/process')
async def process_data(request: DataRequest):
    result = data_endpoint.handle_request(request.dict())

    if not result['success']:
        raise HTTPException(
            status_code=400,
            detail=result['error']
        )

    return result
```
