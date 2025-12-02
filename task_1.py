class HashTable:

    def __init__(self, size=100):
        self.size = size
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key):
        return hash(key) % self.size

    def set(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def get(self, key, default=None):
        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v
        return default

    def delete(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False

if __name__ == "__main__":
    ht = HashTable(size=10)
    ht.set("apple", 10)
    ht.set("banana", 20)

    print(ht.get("apple"))
    print(ht.delete("apple"))
    print(ht.get("apple"))
    print(ht.delete("apple"))
