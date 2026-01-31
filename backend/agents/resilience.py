import time
import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger("Circuit-Breaker")

class CircuitBreakerOpenException(Exception):
    """Exception raised when the circuit breaker is open."""
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED" # CLOSED, OPEN, HALF-OPEN

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF-OPEN"
                    logger.info("Circuit Breaker transitioned to HALF-OPEN.")
                else:
                    raise CircuitBreakerOpenException(f"Circuit for {func.__name__} is currently OPEN.")

            try:
                result = await func(*args, **kwargs)
                if self.state == "HALF-OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                    logger.info(f"Circuit for {func.__name__} successfully CLOSED.")
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                logger.error(f"Failure {self.failure_count} in {func.__name__}: {str(e)}")
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    logger.critical(f"Circuit for {func.__name__} is now OPEN.")
                raise e
        return wrapper
