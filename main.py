"""
HW05 — City Bike Registry (Resizing Chaining Map)
"""

class HashMap:
    """Chaining hash map with auto-resize at load factor > 0.75."""

    def __init__(self, m=4):
        # Create m empty buckets and size counter
        self.buckets = [[] for _ in range(m)]
        self.count = 0

    def _hash(self, s):
        """Return a simple integer hash for string s."""
        return sum(ord(ch) for ch in s)

    def _index(self, key, m=None):
        """Return bucket index for key with current or given bucket count."""
        if m is None:
            m = len(self.buckets)
        return self._hash(key) % m

    def __len__(self):
        """Return number of stored pairs."""
        return self.count

    def _resize(self, new_m):
        """Resize to new_m buckets and rehash all pairs."""
        old_buckets = self.buckets
        self.buckets = [[] for _ in range(new_m)]
        self.count = 0  # will re-add each pair
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)  # reinsert into new buckets

    def put(self, key, value):
        """Insert or overwrite. Resize first if load will exceed 0.75."""
        # Check load factor
        if (self.count + 1) / len(self.buckets) > 0.75:
            self._resize(len(self.buckets) * 2)

        index = self._index(key)
        bucket = self.buckets[index]

        # Check if key exists → overwrite
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return

        # Otherwise append new pair
        bucket.append([key, value])
        self.count += 1

    def get(self, key):
        """Return value for key or None if missing."""
        index = self._index(key)
        bucket = self.buckets[index]

        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return None

    def delete(self, key):
        """Remove key if present. Return True if removed else False."""
        index = self._index(key)
        bucket = self.buckets[index]

        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                self.count -= 1
                return True
        return False


if __name__ == "__main__":
    # Optional manual check
    hm = HashMap(2)
    hm.put("bike1", "stationA")
    hm.put("bike2", "stationB")
    hm.put("bike3", "stationC")  # triggers resize
    print(len(hm))  # 3
    print(hm.get("bike2"))  # stationB
    hm.delete("bike1")
    print(len(hm))  # 2
    print(hm.get("bike1"))  # None
