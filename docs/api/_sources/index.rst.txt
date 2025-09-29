DevToolkit Python Tools Documentation
=====================================

Welcome to the DevToolkit Python Tools documentation. This comprehensive guide covers the plugin architecture, individual tools, and development patterns.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   tools
   api
   development
   testing

Overview
--------

DevToolkit Python Tools is a collection of developer utilities built with a plugin architecture. Each tool provides:

- **Pydantic Validation**: Type-safe input/output models
- **JSON API**: Structured responses for integration
- **CLI Interface**: Command-line access for automation
- **Comprehensive Testing**: Full test coverage for reliability

Quick Start
-----------

.. code-block:: bash

   # Install dependencies
   pip install pydantic

   # List all tools
   python3 devtools.py list

   # Use a tool
   python3 devtools.py base64 "hello world"

   # Get tool information
   python3 devtools.py info base64

Architecture
------------

The plugin system consists of:

.. code-block:: text

   python-tools/
   ├── core/              # Plugin framework
   │   ├── __init__.py
   │   └── base.py        # BaseTool, Registry, Models
   ├── plugins/           # Tool implementations
   │   ├── __init__.py    # Auto-registration
   │   ├── base64_tool.py
   │   ├── url_tool.py
   │   └── ...
   ├── tests/             # Comprehensive test suite
   └── devtools.py        # CLI interface

Available Tools
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Tool
     - Category  
     - Description
   * - base64
     - encoding
     - Encode/decode Base64 strings with validation
   * - url
     - encoding
     - Encode/decode URL strings with validation warnings
   * - hash
     - security
     - Generate MD5, SHA1, SHA256, SHA512 hashes
   * - jwt
     - security
     - Decode and analyze JSON Web Tokens
   * - json
     - text
     - Format, validate, and minify JSON
   * - uuid
     - text
     - Generate UUID v1/v4 identifiers
   * - epoch
     - time
     - Convert Unix timestamps to readable formats
   * - color
     - design
     - Convert between HEX, RGB, HSL color formats

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`