# Premium Data Payload Handler

This project provides functionality to generate, compare, and validate **Premium** data payloads according to a specified schema. The service is built using **FastAPI** for efficient and scalable API access.

## Features

- **Payload Generation**  
  Generate valid *Premium* data payloads that conform to the required schema.

- **Payload Comparison**  
  Compare two *Premium* payloads to determine if they are equivalent.

- **Payload Validation** *(Optional)*  
  Validate whether a given payload conforms to the defined schema.

## Methods

### `PremiumGenerator.generate_premium() -> Premium`

Generates a valid Premium payload that conforms to the given schema.

- **Returns:**  
  A valid Premium payload.

---

### `PremiumComparator.are_equal(payload1: Union[Dict, str],payload2: Union[Dict, str], tolerance: float = 0.01) -> bool)`

Compares two Premium payloads for equivalence.

- **Parameters:**
  - `payload1` *(dict)*: The first Premium payload.
  - `payload2` *(dict)*: The second Premium payload.
- **Returns:**  
  `True` if the payloads are equivalent, `False` otherwise.

---

### `PremiumValidator.validate_with_errors(payload: Union[Dict, str]) -> Optional[List[str]]`

Validates whether a given payload conforms to the specified schema.

- **Parameters:**
  - `payload` *(dict)*: The payload to validate.
- **Returns:**  
  `None` if the payload is valid, `Specific Error` otherwise.

---



## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:yeefongwu/mercury.git
2. **Install dependencies**
    ```bash
    pip install fastapi uvicorn pydantic
3. **Run FastAPI server**
    ```bash
    uvicorn main:app --reload
4. **Access the API docs**
    
    Open your browser and go to: http://localhost:8000/docs



## Usage

### 🔹 GET `/generate`

**Description:** Generate a valid Premium payload based on the provided schema.Data will be stored in premiums.json

**Curl Example:**
```bash
curl "http://127.0.0.1:8000/premiums/generate" 
```

### 🔹 POST `/compare`

**Description:** Compare 2 Premium payload.

**Curl Example:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/premiums/compare?id1={your_id}&id2={your_id}&tolerance={your_tolerance}' \
  -H 'accept: application/json'
  ```
### 🔹 POST `/validate`

**Description:** Validate a Premium payload based on the provided schema.

**Curl Example:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/premiums/validate?id={your_id}' \
  -H 'accept: application/json'
