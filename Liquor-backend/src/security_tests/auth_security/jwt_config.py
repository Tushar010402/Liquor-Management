"""
JWT configuration for security tests.
"""

# JWT configuration
JWT_SECRET_KEY = 'test_secret_key'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = 3600  # 1 hour in seconds
