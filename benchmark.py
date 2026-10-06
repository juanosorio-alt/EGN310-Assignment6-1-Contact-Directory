"""Fair, repeated exact-name lookup measurements on identical contact data."""
from random import Random
from statistics import median
from time import perf_counter_ns
from bst import Contact, ContactBST, normalize


def linear_search(contacts: list[Contact], name: str) -> Contact | None:
    key = normalize(name)
    for contact in contacts:
        if contact.key == key:
            return contact
    return None


def demo_tree(count: int = 15) -> ContactBST:
    contacts = [Contact(f"Contact {i:05d}", f"555-{i:04d}", f"contact{i}@example.com")
                for i in range(count)]
    Random(61).shuffle(contacts)
    tree = ContactBST()
    for contact in contacts:
        tree.insert(contact)
    return tree


def compare(tree: ContactBST, query_count: int = 200, trials: int = 5) -> dict:
    if not len(tree):
        raise ValueError("Add contacts before running the comparison.")
    if query_count < 2 or trials < 1:
        raise ValueError("Use at least two queries and one trial.")
    # Snapshot the SAME records; shuffle outside timing to avoid alphabetical bias.
    contacts = list(tree.inorder())
    rng = Random(61)
    rng.shuffle(contacts)
    missing = "__missing_contact__"
    while tree.search(missing) is not None:
        missing += "_"
    queries = [rng.choice(contacts).name if i % 2 == 0 else missing
               for i in range(query_count)]
    rng.shuffle(queries)
    lookups = {"BST": tree.search, "Linear scan": lambda name: linear_search(contacts, name)}
    # Warm up and verify equality before measuring.
    expected = [linear_search(contacts, q) for q in queries]
    assert [tree.search(q) for q in queries] == expected
    samples = {label: [] for label in lookups}
    for trial in range(trials):
        order = list(lookups) if trial % 2 == 0 else list(reversed(lookups))
        for label in order:
            lookup = lookups[label]
            start = perf_counter_ns()
            for query in queries:
                lookup(query)
            samples[label].append((perf_counter_ns() - start) / 1_000_000)
    return {"contacts": len(contacts), "height": tree.height(), "queries": len(queries),
            "hits": sum(c is not None for c in expected), "trials": trials,
            "rows": [{"Method": label, "Median batch (ms)": median(values),
                      "Mean per lookup (µs)": median(values) * 1000 / len(queries)}
                     for label, values in samples.items()], "samples_ms": samples}
