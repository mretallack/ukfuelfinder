#!/usr/bin/env python3
"""
Example: Using Global Backward Compatibility Configuration

This example demonstrates how to use the global configuration option
to control backward compatibility for all client instances.
"""

import ukfuelfinder

# Set backward compatibility globally for all clients
ukfuelfinder.set_global_backward_compatible(False)

# All clients created after this will have backward_compatible=False
# regardless of constructor parameters or environment variables
client1 = ukfuelfinder.FuelFinderClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    backward_compatible=True  # This will be overridden by global config
)

client2 = ukfuelfinder.FuelFinderClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

print(f"Client 1 backward_compatible: {client1.backward_compatible}")  # False
print(f"Client 2 backward_compatible: {client2.backward_compatible}")  # False

# You can change the global setting at any time
ukfuelfinder.set_global_backward_compatible(True)

client3 = ukfuelfinder.FuelFinderClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

print(f"Client 3 backward_compatible: {client3.backward_compatible}")  # True

# Priority order:
# 1. Global configuration (highest priority)
# 2. Environment variable UKFUELFINDER_BACKWARD_COMPATIBLE
# 3. Constructor parameter backward_compatible
# 4. Default value (True)
