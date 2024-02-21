# Starling Bank Round-up Feature

This project implements a "round-up" feature for Starling Bank customers using the public developer API. The feature rounds up transactions to the nearest pound and transfers the difference into a savings goal, helping customers save for future adventures.

## Project Structure

The project is structured as follows:

- `main`:
  - `__init__.py`: An empty file that tells Python that this directory should be considered a Python package.
  - `main.py`: The main script that demonstrates the round-up feature.
  - `starling_bank_client.py`: A Python class that interacts with the Starling Bank API.
  - `utils.py`: Utility functions used by the main script and the StarlingBankClient class.

- `tests`:
  - `__init__.py`: A file that adds the current directory and the `main` directory to the Python path.
  - `test_starling_bank_client.py`: Unit tests for the StarlingBankClient class.


## Setup

1. Clone the repository:

```
git clone git@github.com:IsmailDoghri/RoundUpChallenge.git
```

2. Obtain an access token from the Starling Developer Portal and set it as an environment variable:

```
export STARLING_ACCESS_TOKEN="your-access-token"
```


## Usage

Run the main script to see the round-up feature in action:

 ```
python main/main.py
```


## Testing

Run the unit tests using pytest:

```
pytest tests/
```
