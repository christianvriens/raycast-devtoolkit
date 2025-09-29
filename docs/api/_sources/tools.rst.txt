Tool Reference
==============

This section provides detailed documentation for each tool, including input/output models, validation rules, and examples.

Base64 Tool
-----------

.. automodule:: plugins.base64_tool
   :members:
   :undoc-members:
   :show-inheritance:

**Input Model**: Base64Input

- ``text`` (str): Text to encode or decode
- ``operation`` (str): "encode" or "decode"

**Output Model**: Base64Output  

- ``input`` (str): Original input text
- ``output`` (str): Encoded or decoded result
- ``operation`` (str): Operation performed

**Examples**:

.. code-block:: python

   # Encoding
   input_data = Base64Input(text="hello", operation="encode")
   result = tool.execute(input_data)
   # result.output == "aGVsbG8="

   # Decoding
   input_data = Base64Input(text="aGVsbG8=", operation="decode") 
   result = tool.execute(input_data)
   # result.output == "hello"

URL Tool
--------

.. automodule:: plugins.url_tool
   :members:
   :undoc-members:
   :show-inheritance:

**Input Model**: UrlInput

- ``text`` (str): Text to encode or decode
- ``operation`` (str): "encode" or "decode"

**Output Model**: UrlOutput

- ``input`` (str): Original input text
- ``output`` (str): Encoded or decoded result  
- ``operation`` (str): Operation performed
- ``is_valid_url`` (bool): Whether result is a valid URL

**Validation**:
- Warns when decoding text without % characters
- Validates URL format in results

Hash Tool
---------

.. automodule:: plugins.hash_tool
   :members:
   :undoc-members:
   :show-inheritance:

**Input Model**: HashInput

- ``text`` (str): Text to hash
- ``algorithm`` (str): Hash algorithm (md5, sha1, sha256, sha512)

**Output Model**: HashOutput

- ``input`` (str): Original input text
- ``algorithm`` (str): Algorithm used
- ``hash`` (str): Generated hash
- ``length`` (int): Hash length in characters

**Algorithms**:
- **MD5**: 32 characters (deprecated for security)
- **SHA1**: 40 characters (deprecated for security)  
- **SHA256**: 64 characters (recommended)
- **SHA512**: 128 characters (high security)

JWT Tool
--------

.. automodule:: plugins.jwt_tool
   :members:
   :undoc-members:
   :show-inheritance:

**Input Model**: JWTInput

- ``token`` (str): JWT token to decode

**Output Model**: JWTOutput

- ``header`` (dict): JWT header
- ``payload`` (dict): JWT payload
- ``signature`` (str): JWT signature
- ``issued_at`` (int, optional): Issued timestamp
- ``expires_at`` (int, optional): Expiration timestamp
- ``issued_at_readable`` (str, optional): Human-readable issued time
- ``expires_at_readable`` (str, optional): Human-readable expiration
- ``is_expired`` (bool, optional): Whether token is expired
- ``valid_format`` (bool): Whether JWT format is valid

**Features**:
- Decodes JWT header and payload
- Analyzes expiration claims (exp, iat)
- Provides human-readable timestamps
- Validates JWT format

JSON Tool
---------

.. automodule:: plugins.json_tool
   :members:
   :undoc-members:
   :show-inheritance:

**Input Model**: JSONInput

- ``text`` (str): JSON text to format or minify
- ``minify`` (bool): Whether to minify instead of format

**Output Model**: JSONOutput

- ``formatted`` (str): Formatted or minified JSON
- ``original`` (str): Original input
- ``operation`` (str): "format" or "minify"
- ``valid`` (bool): Whether input was valid JSON
- ``size_before`` (int): Size before processing
- ``size_after`` (int): Size after processing
- ``parsed_data`` (dict): Parsed JSON structure

**Operations**:
- **Format**: Pretty-print with indentation and sorting
- **Minify**: Remove whitespace and formatting

UUID Tool
---------

.. automodule:: plugins.uuid_tool
   :members:
   :undoc-members:
   :show-inheritance:

**Input Model**: UUIDInput

- ``version`` (int): UUID version (1 or 4), default 4
- ``count`` (int): Number of UUIDs to generate (1-100), default 1

**Output Model**: UUIDOutput

- ``uuids`` (List[str]): Generated UUIDs
- ``version`` (int): UUID version used
- ``count`` (int): Number of UUIDs generated
- ``format`` (str): UUID format description

**UUID Versions**:
- **v1**: Time-based, includes MAC address and timestamp
- **v4**: Random, recommended for general use

Epoch Tool
----------

.. automodule:: plugins.epoch_tool
   :members:
   :undoc-members:
   :show-inheritance:

**Input Model**: EpochInput

- ``timestamp`` (str, optional): Epoch timestamp, empty for current time

**Output Model**: EpochOutput

- ``epoch`` (int): Unix timestamp
- ``utc`` (dict): UTC time representations
- ``local`` (dict): Local time representations  
- ``relative`` (dict): Relative time information

**Time Formats**:
- **readable**: "2022-01-01 12:00:00 UTC"
- **iso**: "2022-01-01T12:00:00+00:00"
- **ddmmyyyy**: "01/01/2022 12:00:00"

**Features**:
- Handles seconds and milliseconds
- Provides multiple time formats
- Calculates relative time differences
- Supports timezone conversion

Color Tool
----------

.. automodule:: plugins.color_tool
   :members:
   :undoc-members:
   :show-inheritance:

**Input Model**: ColorInput

- ``color`` (str): Color value in any supported format

**Output Model**: ColorOutput

- ``input_color`` (str): Original input
- ``input_format`` (str): Detected format (hex, rgb, hsl)
- ``hex`` (str): Hexadecimal representation
- ``rgb`` (dict): RGB values {r, g, b}
- ``hsl`` (dict): HSL values {h, s, l}
- ``css_rgb`` (str): CSS rgb() format
- ``css_hsl`` (str): CSS hsl() format

**Supported Formats**:
- **HEX**: #FF0000, #f00, FF0000
- **RGB**: rgb(255, 0, 0)
- **HSL**: hsl(0, 100%, 50%)

**Validation**:
- Validates color format and values
- Converts between all supported formats
- Provides CSS-ready output

Tool Configuration
------------------

Each tool provides metadata through its configuration:

.. code-block:: python

   config = tool.get_config()
   print(config.name)        # Tool name
   print(config.description) # Tool description  
   print(config.category)    # Category (encoding, security, etc.)
   print(config.keywords)    # Search keywords
   print(config.version)     # Tool version

Schema Generation
-----------------

All tools provide JSON schemas for their input/output models:

.. code-block:: python

   tool = registry.get_tool('base64')
   
   input_schema = tool.get_input_schema()
   output_schema = tool.get_output_schema()
   
   # Schemas are standard JSON Schema format
   print(input_schema['properties'])
   print(output_schema['properties'])