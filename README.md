# Vulnerability Version Checker API

## Overview
The Vulnerability Version Checker API provides a service to identify vulnerable library versions based on data from the osv.dev database.

## Features
- Fetch and list all vulnerable versions of a specified package.
- Support for Debian and Ubuntu ecosystems.
- Real-time querying using the osv.dev API.
- Response includes a timestamp for each query to ensure data freshness.


## Installation

### Prerequisites
- Python 3.8 or higher
- pip for package installation

Clone the repository and install the required dependencies
    ```bash
    git clone https://github.com/algaziev7/homeworkMSCi.git
    cd your-project-directory
    ```

```bash
pip install -r requirements.txt
```


## Usage

To run the application, execute the following command:
```bash
uvicorn app.main:app --reload
```

