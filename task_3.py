import timeit
from typing import List, Tuple, Callable


# ---------- KMP (Knuth-Morris-Pratt) ----------

def kmp_prefix_function(pattern: str) -> List[int]:
    lps = [0] * len(pattern)
    j = 0 

    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]

        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    return lps


def kmp_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0

    lps = kmp_prefix_function(pattern)
    j = 0

    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == len(pattern):
            return i - j + 1

    return -1


# ---------- Rabin-Karp ----------

def rabin_karp_search(text: str, pattern: str, prime: int = 101) -> int:
    n = len(text)
    m = len(pattern)

    if m == 0:
        return 0
    if m > n:
        return -1

    base = 256
    h = pow(base, m - 1, prime)

    pattern_hash = 0
    text_hash = 0

    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        text_hash = (base * text_hash + ord(text[i])) % prime

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            text_hash = (text_hash - ord(text[i]) * h) % prime
            text_hash = (text_hash * base + ord(text[i + m])) % prime
            text_hash = (text_hash + prime) % prime

    return -1


# ---------- Boyer-Moore (bad character rule only) ----------

def build_bad_char_table(pattern: str) -> dict:
    table = {}
    length = len(pattern)
    for i in range(length):
        table[pattern[i]] = max(1, length - i - 1)
    return table


def boyer_moore_search(text: str, pattern: str) -> int:
    n = len(text)
    m = len(pattern)

    if m == 0:
        return 0
    if m > n:
        return -1

    bad_char_table = build_bad_char_table(pattern)
    i = 0

    while i <= n - m:
        j = m - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        bad_char = text[i + j]
        shift = bad_char_table.get(bad_char, m)
        i += shift

    return -1


# ---------- Benchmark helper ----------

def load_text(file_path: str) -> str:
    """Load text from file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def benchmark_algorithm(
    algorithm: Callable[[str, str], int],
    text: str,
    pattern: str,
    repeat: int = 5
) -> float:

    def wrapper():
        algorithm(text, pattern)

    t = timeit.timeit(wrapper, number=repeat)
    return t / repeat


def run_benchmarks():
    article1_path = "article1.txt"
    article2_path = "article2.txt"

    text1 = load_text(article1_path)
    text2 = load_text(article2_path)

    existing_pattern_1 = "the"
    fake_pattern_1 = "qwertyqwerty"

    existing_pattern_2 = "and"
    fake_pattern_2 = "asdfghzxcv"

    algorithms = {
        "Boyer-Moore": boyer_moore_search,
        "KMP": kmp_search,
        "Rabin-Karp": rabin_karp_search,
    }

    print("=== Article 1 ===")
    for name, algo in algorithms.items():
        t_exist = benchmark_algorithm(algo, text1, existing_pattern_1)
        t_fake = benchmark_algorithm(algo, text1, fake_pattern_1)
        print(f"{name}: existing = {t_exist:.6f}s, fake = {t_fake:.6f}s")

    print("\n=== Article 2 ===")
    for name, algo in algorithms.items():
        t_exist = benchmark_algorithm(algo, text2, existing_pattern_2)
        t_fake = benchmark_algorithm(algo, text2, fake_pattern_2)
        print(f"{name}: existing = {t_exist:.6f}s, fake = {t_fake:.6f}s")


if __name__ == "__main__":
    run_benchmarks()
