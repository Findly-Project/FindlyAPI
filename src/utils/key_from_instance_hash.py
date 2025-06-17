def key_from_instance_hash(func, self):
    instance_hash = hash(self)
    return f"{func.__module__}.{func.__name__}:{instance_hash}"
