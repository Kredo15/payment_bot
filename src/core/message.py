class LogMessages:
    """Internal log messages"""

    CREATE_INVOICE = "Create invoice for subscription {name} by {method} user: {user_id}"
    PAID_INVOICE = "Paid invoice for subscription {name} by {method} user: {user_id}"
    FAILED_INVOICE = "Failed invoice for subscription {name} by {method} user: {user_id}"
    INVALID_INVOICE = "Invalid invoice metadata by {method}: {request}"
    INVALID_JSON = "Invalid JSON {request}"
