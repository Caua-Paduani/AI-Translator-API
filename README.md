# FastAPI CEP Lookup API

This project is a simple and efficient API for looking up Brazilian postal codes (CEP) using [ViaCEP](https://viacep.com.br/). It is built with [FastAPI](https://fastapi.tiangolo.com/) and includes local in-memory caching and input validation for performance and reliability.

## Features
- **CEP Lookup**: Fetches address data for a given Brazilian CEP using the ViaCEP API.
- **Input Validation**: Ensures only valid CEPs (8 numeric digits) are processed.
- **Local Cache**: Stores recent CEP lookups in memory for 1 hour to speed up repeated requests and reduce external API calls.
- **Error Handling**: Returns clear error messages for invalid or not found CEPs.

## How It Works
1. **Validation**: The API receives a CEP, removes all non-numeric characters, and checks if it has exactly 8 digits.
2. **Cache Check**: Before making an external request, it checks if the CEP is already in the local cache and if the cached data is still valid (not expired).
3. **ViaCEP Request**: If not cached, it fetches the data from the ViaCEP API.
4. **Cache Storage**: The result is stored in the cache with a timestamp.
5. **Response**: Returns the address data as JSON.

## Endpoint
### `GET /buscar-cep?cep=<CEP>`
- **Query Parameter:** `cep` (string) — The Brazilian postal code to look up.
- **Returns:** JSON with address data or an error message.

#### Example Request
```
GET http://localhost:8000/buscar-cep?cep=30140-071
```

#### Example Response (Success)
```json
{
  "cep": "30140-071",
  "logradouro": "Praça Sete de Setembro",
  "complemento": "",
  "bairro": "Centro",
  "localidade": "Belo Horizonte",
  "uf": "MG",
  "ibge": "3106200",
  "gia": "",
  "ddd": "31",
  "siafi": "4123"
}
```

#### Example Response (Invalid CEP)
```json
{
  "detail": "CEP must have 8 digits"
}
```

#### Example Response (Not Found)
```json
{
  "detail": "Invalid or not found CEP"
}
```

## How to Run
1. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn requests
   ```
2. **Start the server:**
   ```bash
   uvicorn main:app --reload
   ```
3. **Access the API docs:**
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser for interactive documentation.

## How the Cache Works
- The cache is a Python dictionary declared as `cache = {}`.
- Each key is a cleaned CEP string (only digits).
- Each value is another dictionary with:
  - `'data'`: the address data returned by ViaCEP
  - `'timestamp'`: the time (in seconds) when the data was cached
- When a request is made:
  - If the CEP is in the cache and the data is less than 1 hour old, the cached data is returned.
  - Otherwise, a new request is made to ViaCEP and the result is cached.

## How the Validation Works
- The function `validate_cep` removes all non-digit characters from the input.
- It checks if the result has exactly 8 digits.
- If not, it raises an HTTP 400 error with a clear message.

## License
MIT 