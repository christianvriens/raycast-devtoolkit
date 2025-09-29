Quick Start Guide
=================

Installation
------------

DevToolkit Python Tools requires Python 3.7+ and Pydantic:

.. code-block:: bash

   # Install Pydantic
   pip install pydantic

   # Clone or download the tools
   git clone <repository-url>
   cd python-tools

Basic Usage
-----------

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

The main interface is through ``devtools.py``:

.. code-block:: bash

   # List all available tools
   python3 devtools.py list

   # Get detailed information about a tool
   python3 devtools.py info base64

   # Use a tool (legacy API)
   python3 devtools.py base64 "hello world"

   # Use a tool (modern plugin API)
   python3 devtools.py run base64 '{"text":"hello","operation":"encode"}'

Tool Categories
~~~~~~~~~~~~~~~

Tools are organized into categories:

- **encoding**: Base64, URL encoding/decoding
- **security**: Hashing, JWT token analysis  
- **text**: JSON formatting, UUID generation
- **time**: Timestamp conversion
- **design**: Color format conversion

Examples by Tool
----------------

Base64 Tool
~~~~~~~~~~~

.. code-block:: bash

   # Encode text
   python3 devtools.py base64 "hello world"
   # Output: {"input": "hello world", "output": "aGVsbG8gd29ybGQ=", "operation": "encode"}

   # Decode Base64
   python3 devtools.py base64 "aGVsbG8gd29ybGQ=" --decode
   # Output: {"input": "aGVsbG8gd29ybGQ=", "output": "hello world", "operation": "decode"}

JWT Tool
~~~~~~~~

.. code-block:: bash

   # Decode JWT token
   python3 devtools.py jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   # Output: Complete JWT analysis with header, payload, expiration info

Hash Tool
~~~~~~~~~

.. code-block:: bash

   # Generate SHA256 hash (default)
   python3 devtools.py hash "secret"

   # Generate MD5 hash
   python3 devtools.py hash "secret" --algorithm md5

   # All algorithms: md5, sha1, sha256, sha512

URL Tool
~~~~~~~~

.. code-block:: bash

   # URL encode
   python3 devtools.py url "hello world"
   # Output: {"input": "hello world", "output": "hello%20world", "operation": "encode", "is_valid_url": false}

   # URL decode  
   python3 devtools.py url "hello%20world" --decode

JSON Tool
~~~~~~~~~

.. code-block:: bash

   # Format JSON
   python3 devtools.py json '{"name":"John","age":30}'

   # Minify JSON
   python3 devtools.py json '{"name": "John", "age": 30}' --minify

UUID Tool
~~~~~~~~~

.. code-block:: bash

   # Generate single UUID v4
   python3 devtools.py uuid

   # Generate multiple UUIDs
   python3 devtools.py uuid --count 5

   # Generate UUID v1
   python3 devtools.py uuid --version 1

Epoch Tool
~~~~~~~~~~

.. code-block:: bash

   # Convert current timestamp
   python3 devtools.py epoch

   # Convert specific timestamp
   python3 devtools.py epoch 1640995200

   # Supports millisecond timestamps
   python3 devtools.py epoch 1640995200000

Color Tool
~~~~~~~~~~

.. code-block:: bash

   # Convert HEX color
   python3 devtools.py color "#ff0000"

   # Convert RGB color
   python3 devtools.py color "rgb(255, 0, 0)"

   # Convert HSL color
   python3 devtools.py color "hsl(0, 100%, 50%)"

Programming Interface
---------------------

Python Integration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from core import registry

   # Get a tool instance
   base64_tool = registry.get_tool('base64')

   # Validate and execute
   input_data = base64_tool.validate_input({
       "text": "hello world",
       "operation": "encode"
   })
   
   result = base64_tool.execute(input_data)
   print(result.output)  # "aGVsbG8gd29ybGQ="

JSON API
~~~~~~~~

All tools return structured JSON responses suitable for automation:

.. code-block:: json

   {
     "input": "hello world",
     "output": "aGVsbG8gd29ybGQ=",
     "operation": "encode",
     "metadata": {
       "length": 16,
       "valid": true
     }
   }

Error Handling
--------------

Tools provide detailed error information:

.. code-block:: bash

   # Invalid input example
   python3 devtools.py base64 ""
   # Error: Text cannot be empty

   # Invalid JSON example  
   python3 devtools.py json "invalid json"
   # Error: Invalid JSON: Expecting value: line 1 column 1 (char 0)

Testing
-------

Run the comprehensive test suite:

.. code-block:: bash

   # Run all tests
   python3 tests/run_all_tests.py

   # Run specific tool tests
   python3 tests/test_base64_tool.py

   # Test output example:
   # 🧪 Running DevToolkit Plugin Tests
   # ==================================================
   # test_encode_basic ... ok
   # test_decode_basic ... ok
   # ...
   # 🎉 All tests passed!