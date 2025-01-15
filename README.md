# Credit Rating API

## Project Overview

This project is designed to compute the credit rating for Residential Mortgage-Backed Securities (RMBS). It evaluates the creditworthiness of a collection of mortgages based on several factors, including credit scores, loan-to-value (LTV) ratios, debt-to-income (DTI) ratios, loan types, and property types.

### Key Features:

- **Input**: Accepts a JSON payload of mortgage details.
- **Output**: Returns a credit rating (e.g., "AAA", "BBB", "C").
- **Extensible**: Modular design allows future enhancements like additional attributes or optimization techniques.
- **Tested**: Includes unit tests to ensure robustness and accuracy.

---

## Project Structure

The directory structure is as follows:

```
credit-rating-api/
│
├── configs/
│   ├── __init__.py          # Initialization module
│   ├── config.py            # Handles configuration settings
│   ├── constants.py         # Stores global constants
│   ├── config.ini           # Configurable settings
│
├── controllers/
│   ├── __init__.py
│   ├── rating_controller.py # API endpoint controller logic
│
├── domain/
│   ├── __init__.py
│   ├── credit_rating.py     # Core logic for credit rating calculations
│
├── log/
│   ├── credit_rating_api.log # Log file for tracking application activity
│
├── routes/
│   ├── __init__.py
│   ├── rating_route.py      # Routing logic for API requests
│
├── schemas/
│   ├── __init__.py
│   ├── rmbs.py              # Schema definitions for input validation
│
├── tests/
│   ├── test_credit_rating.py # Unit tests for credit rating calculations
│   ├── test_rating_route.py  # Unit tests for API endpoints
│
├── utils/
│   ├── __init__.py
│   ├── decorators.py        # Utility decorators for error handling, logging, etc.
│   ├── error_handlers.py    # Centralized error handling
│   ├── logger.py            # Logging utility
│   ├── response.py          # Helper functions for formatting API responses
│
├── .env                     # Environment variables
├── .gitignore               # Git ignore file
├── Dockerfile               # Docker configuration
├── main.py                  # Entry point of the application
├── README.md                # Documentation (this file)
└── requirements.txt         # Dependencies
```

---

## Installation and Setup

### Prerequisites:

- Python 3.8+
- Virtual environment (optional, but recommended)

### Steps:

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd credit-rating-api
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment:

   - Add required environment variables in the `.env` file.

4. Start the application:

   ```bash
   python main.py
   ```

---

## Usage

### API Endpoint

#### Calculate Credit Rating

- **Endpoint**: `/calculate_credit_rating`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "mortgages": [
      {
        "credit_score": 750,
        "loan_amount": 200000,
        "property_value": 250000,
        "annual_income": 60000,
        "debt_amount": 20000,
        "loan_type": "fixed",
        "property_type": "single_family"
      }
    ]
  }
  ```
- **Response**:
  ```json
  {
      "data": {
          "credit_rating": "C"
      },
      "msg": "Credit rating calculation successful",
      "status_code": 200
  }
  ```

---

## Testing

Run the unit tests using `unittest`:

```bash

```

Tests include:

- Valid mortgage cases
- Edge cases (e.g., missing attributes, invalid values)
- End-to-end API functionality

---
## Docker

### Build and Run with Docker
1. **Build the Image**:
   ```bash
   docker build -t credit-rating-api .
   ```

2. **Run the Container**:
   ```bash
   docker run -p 5000:5000 credit-rating-api
   ```

3. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

---
## Technical Details

### Rating Calculation Logic

The rating is based on:

1. **Loan-to-Value (LTV) Ratio**
2. **Debt-to-Income (DTI) Ratio**
3. **Credit Score**
4. **Loan Type**
5. **Property Type**
6. **Average Credit Score**

The algorithm calculates a risk score for each mortgage and aggregates it to determine the final rating:

- **AAA**: Total Score ≤ 2
- **BBB**: Total Score 3-5
- **C**: Total Score > 5

### Error Handling

- **Validation Errors**: Invalid or missing attributes result in a 400 Bad Request.
- **Server Errors**: Unexpected issues return a 500 Internal Server Error.

---

## Future Enhancements

- Optimize for high volumes of requests.
- Implement security features (e.g., authentication, data encryption).

---
