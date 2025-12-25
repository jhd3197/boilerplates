"""Playground for testing MyProject boilerplate.

This module demonstrates the usage of the MyProject boilerplate,
showcasing all the features and capabilities of the Client class
and all its mixins.
"""

from myproject import Client


def separator(title: str) -> None:
    """Print a visual separator with title."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def test_basic_initialization():
    """Test basic Client initialization."""
    separator("1. Basic Client Initialization")

    # Create instance with default settings
    client = Client()
    print(f"Created: {client}")
    print(f"Repr: {repr(client)}")
    print(f"MRO: {' -> '.join(client.get_info()['mro'][:7])}")


def test_custom_initialization():
    """Test initialization with custom configuration."""
    separator("2. Custom Initialization with Config")

    # Create instance with custom config
    client = Client(
        name="CustomApp",
        version="2.0.0",
        config={
            "env": "production",
            "debug": False,
            "log_level": "INFO",
            "timeout": 60,
            "custom_settings": {"feature_flag": True},
        },
        cache_folder="custom_cache",
        api_base_url="https://api.example.com",
    )

    print(f"Created: {client}")
    print(f"Cache folder: {client.cache_folder}")
    print(f"API base URL: {client.api_base_url}")
    client.print_config()


def test_logging_operations():
    """Test logging operations."""
    separator("3. Logging Operations")

    client = Client(name="LoggerDemo", config={"log_level": "DEBUG"})

    # Test different log levels
    client.debug("This is a debug message", {"module": "playground"})
    client.info("Application started successfully")
    client.warning("This is a warning message", {"code": "WARN001"})
    client.error("An error occurred", {"error_code": 500})

    # Change log level
    print("\n--- Changing log level to ERROR ---")
    client.set_log_level("ERROR")
    client.debug("This won't be logged")
    client.info("This won't be logged either")
    client.error("Only this error will be logged")


def test_cache_operations():
    """Test cache operations."""
    separator("4. Cache Operations")

    client = Client(name="CacheDemo", cache_folder="test_cache")

    # Set cache values
    client.cache_set("user_1", {"name": "John Doe", "email": "john@example.com"})
    client.cache_set("user_2", {"name": "Jane Smith", "email": "jane@example.com"}, persist=True)
    client.cache_set("temp_data", "This will expire", ttl=2)

    print("Cached 3 items (1 persisted to disk)")

    # Get cache values
    result = client.cache_get("user_1")
    print(f"\nRetrieved user_1: {result['data']}")

    result = client.cache_get("user_2", from_disk=True)
    print(f"Retrieved user_2 from disk: {result['data']}")

    # Cache stats
    stats = client.cache_stats()
    print(f"\nCache stats: {stats['data']}")

    # Delete specific cache entry
    client.cache_delete("user_1")
    print("\nDeleted user_1 from cache")

    # Clear all cache
    client.cache_clear(clear_disk=True)
    print("Cleared all cache")


def test_api_operations():
    """Test API operations."""
    separator("5. API Operations")

    client = Client(
        name="APIDemo",
        api_base_url="https://api.example.com",
        api_key="test_api_key_12345"
    )

    # Test GET request
    result = client.get("/users", params={"page": 1, "limit": 10})
    print(f"GET request: {result['data']}")

    # Test POST request
    result = client.post(
        "/users",
        json_data={"name": "New User", "email": "newuser@example.com"}
    )
    print(f"\nPOST request: {result['data']}")

    # Test PUT request
    result = client.put("/users/123", data={"name": "Updated User"})
    print(f"\nPUT request: {result['data']}")

    # Test DELETE request
    result = client.delete("/users/123")
    print(f"\nDELETE request: {result['data']}")


def test_database_operations():
    """Test database operations."""
    separator("6. Database Operations")

    client = Client(
        name="DatabaseDemo",
        db_url="postgresql://user:pass@localhost/mydb"
    )

    # Connect to database
    result = client.connect_db()
    print(f"Database connection: {result['data']}")

    # Fetch all records
    result = client.db_fetch_all("users", conditions={"active": True})
    print(f"\nFetch query: {result['data']['query']}")

    # Insert record
    result = client.db_insert("users", {"name": "John", "email": "john@example.com"})
    print(f"\nInsert query: {result['data']['query']}")

    # Update record
    result = client.db_update(
        "users",
        {"name": "John Doe"},
        {"email": "john@example.com"}
    )
    print(f"\nUpdate query: {result['data']['query']}")

    # Delete record
    result = client.db_delete("users", {"id": 123})
    print(f"\nDelete query: {result['data']['query']}")

    # Disconnect
    result = client.disconnect_db()
    print(f"\nDisconnection: {result['data']}")


def test_calculation_operations():
    """Test calculation operations from ToolsMixin."""
    separator("7. Tool Operations - Calculations")

    client = Client()

    # Test addition
    result = client.calculate("add", 10, 20, 30)
    print(f"Add (10 + 20 + 30): {result['data']}")

    # Test multiplication
    result = client.calculate("multiply", 5, 4, 3)
    print(f"Multiply (5 * 4 * 3): {result['data']}")

    # Test average
    result = client.calculate("average", 10, 20, 30, 40, 50)
    print(f"Average (10, 20, 30, 40, 50): {result['data']}")


def test_data_operations():
    """Test data formatting, validation, and transformation."""
    separator("8. Tool Operations - Data Processing")

    client = Client()

    data = {
        "name": "John Doe",
        "age": 30,
        "skills": ["Python", "JavaScript"],
    }

    # Format data
    result = client.format_data(data, "pretty_json")
    print(f"Formatted JSON:\n{result['data']}\n")

    # Validate data
    result = client.validate_data(data, ["name", "age"])
    print(f"Validation (name, age): {result['success']}")

    result = client.validate_data(data, ["name", "age", "email"])
    print(f"Validation (name, age, email): {result['success']} - {result.get('error', '')}")

    # Transform data
    result = client.transform_dict(data, key_transform="upper")
    print(f"\nTransformed keys to uppercase: {result['data']}")


def test_client_lifecycle():
    """Test Client initialization and shutdown."""
    separator("9. Client Lifecycle Management")

    client = Client(
        name="LifecycleDemo",
        version="3.0.0",
        db_url="postgresql://localhost/testdb",
        config={"debug": True}
    )

    # Initialize all services
    result = client.initialize()
    print(f"Initialization: {result['data']}")

    # Get status
    result = client.status()
    print(f"\nClient status:")
    for key, value in result['data'].items():
        if key != 'config':
            print(f"  {key}: {value}")

    # Shutdown
    result = client.shutdown()
    print(f"\nShutdown: {result['data']}")


def test_context_manager():
    """Test Client as context manager."""
    separator("10. Context Manager Usage")

    print("Using Client as context manager:")
    with Client(name="ContextDemo", db_url="postgresql://localhost/testdb") as client:
        client.info("Client initialized via context manager")
        client.cache_set("session_data", {"user_id": 123})
        result = client.status()
        print(f"Status inside context: Database connected = {result['data']['database_connected']}")

    print("\nClient automatically shut down after exiting context")


def test_combined_features():
    """Test combining multiple features."""
    separator("11. Combined Features Demo")

    client = Client(
        name="FullFeaturedApp",
        version="1.5.0",
        config={"debug": True, "log_level": "INFO"},
        api_base_url="https://api.example.com",
        cache_folder="app_cache"
    )

    # Log the start
    client.info("Starting combined features demo")

    # Make an API call
    api_result = client.get("/data")
    client.debug("API call completed", {"status": api_result['success']})

    # Cache the result
    if api_result['success']:
        client.cache_set("api_response", api_result['data'], persist=True)
        client.info("API response cached")

    # Retrieve from cache
    cached_result = client.cache_get("api_response")
    client.info("Retrieved data from cache", {"cached": cached_result['success']})

    # Process the data
    if cached_result['success']:
        formatted = client.format_data(cached_result['data'], "pretty_json")
        print(f"\nFormatted cached data:\n{formatted['data']}")

    # Get final stats
    stats = client.cache_stats()
    client.info("Cache stats retrieved", stats['data'])


def test_info_and_mro():
    """Test Client info and MRO."""
    separator("12. Client Info and Method Resolution Order")

    client = Client()
    info = client.get_info()

    print("Client Information:")
    print(f"  Name: {info['name']}")
    print(f"  Version: {info['version']}")
    print(f"  JS Framework: {info['js_framework'] or 'Not set'}")
    print(f"\n  Available Mixins:")
    for mixin in info['available_mixins']:
        print(f"    - {mixin}")

    print(f"\n  Method Resolution Order (MRO):")
    for i, cls in enumerate(info['mro'], 1):
        print(f"    {i}. {cls}")

    print("\n  Explanation:")
    print("  - Client inherits from all 6 mixins")
    print("  - Each mixin calls super().__init__() for cooperative inheritance")
    print("  - Python's MRO ensures each class is initialized exactly once")
    print("  - The chain flows through all mixins before reaching object")


def main():
    """Run all playground tests."""
    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#" + "  MyProject Boilerplate - Client & Mixins Demo".center(68) + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)

    # Run all tests
    test_basic_initialization()
    test_custom_initialization()
    test_logging_operations()
    test_cache_operations()
    test_api_operations()
    test_database_operations()
    test_calculation_operations()
    test_data_operations()
    test_client_lifecycle()
    test_context_manager()
    test_combined_features()
    test_info_and_mro()

    # Final summary
    separator("Summary")
    print("All tests completed successfully!")
    print("\nKey Features Demonstrated:")
    print("  - Cooperative multiple inheritance with 6 mixins")
    print("  - Configuration management (ConfigMixin)")
    print("  - Logging with multiple levels (LoggerMixin)")
    print("  - In-memory and disk caching (CacheMixin)")
    print("  - HTTP API client (APIMixin)")
    print("  - Database operations (DatabaseMixin)")
    print("  - Utility tools (ToolsMixin)")
    print("  - Proper MRO and super() usage")
    print("  - Context manager support")
    print("  - Environment variable configuration")
    print("  - Type hints and comprehensive error handling")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
