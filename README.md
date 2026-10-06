# Assignment 6.1 — Contact Directory

**Author:** Juan Pablo Osorio  
**Course:** EGN 310 — Data Structures  
**Project:** Shipped Application 2

A Streamlit contact directory backed by my own Binary Search Tree implementation.

## Live application

**Deployment URL:** Pending Streamlit Community Cloud publication.

## Features

- Add contacts with name, phone, and email.
- Search by exact name, ignoring case and repeated/leading/trailing whitespace.
- List contacts alphabetically through an inorder BST traversal, without sorting the output.
- Delete contacts, including leaf nodes, nodes with one child, and nodes with two children.
- Compare BST search with linear scan using the same contacts and the same queries.
- Display median batch times, average lookup times, and a timing chart.
- Load 15, 100, 1,000, or 5,000 fictional sample contacts and export the current directory to CSV.

Names serve as unique keys. Duplicate names are rejected without overwriting existing records. Phone and email are optional text fields. Ordering uses Python's case-folded string order, rather than locale-specific collation.

## Run locally

Requires Python 3.12 (tested).

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Quick walkthrough

1. Start with the 15 fictional contacts, or add a contact using the form.
2. Search for `Contact 00003` (an exact, case-insensitive name).
3. Review the ordered directory and optionally download its CSV.
4. Enter a name under Delete, check the confirmation, and delete it.
5. Click **Run timing comparison** to measure searches over the current directory.
6. For a larger comparison, expand **Load a larger sample directory**, choose 1,000 or 5,000, confirm replacement, load the sample, and rerun the benchmark.

## BST implementation

`bst.py` implements `Contact`, `Node`, and `ContactBST` directly. Each node stores one contact plus left and right child references. No library tree or dictionary is used to store the directory. `st.session_state` retains the BST object between Streamlit reruns.

Insert and search follow name comparisons down the tree. Inorder traversal visits left subtree, node, then right subtree. For two-child deletion, the node's contact is replaced by the inorder successor, which is then removed from its original location. Iterative algorithms avoid Python recursion-depth failures in skewed trees.

| Operation | Time | Additional working space |
|---|---|---|
| Insert, search, delete | O(h) | O(1) |
| Inorder traversal | O(n) | O(h) |
| Linear scan | O(n) | O(1) |

Here `n` is the contact count and `h` is tree height. These bounds treat bounded-length name comparisons as constant cost. The tree is not self-balancing: a balanced shape has O(log n) height, but sorted insertion can produce O(n) height and search time. Total tree storage is O(n).

## Timing methodology

`benchmark.py` snapshots the current tree into a list containing exactly the same Contact records. It shuffles the linear list reproducibly outside the timed region. Both methods perform the same 200 queries: 100 successful lookups sampled from existing names and 100 unsuccessful lookups. The missing name is checked to ensure it does not collide with a real contact.

Before timing, the benchmark verifies both methods return identical results. Five trials alternate the measurement order to reduce order effects. `time.perf_counter_ns()` measures each batch; the app displays the median batch time in milliseconds and that median divided by 200 in microseconds per lookup. Dataset generation, traversal, query generation, validation, and rendering are excluded. Both methods use the same name normalization and exact-match semantics.

Results are measurements from the current environment, not fixed claims. Hardware, load, tree shape, and dataset size affect performance. Linear scan can be competitive on small datasets; BST performance is not guaranteed to be faster. The original tree is never modified by benchmarking.

## Data lifetime

This classroom app stores contacts **in memory for the current browser session**, not in a database. A new session or server restart starts with sample contacts. Download CSV before leaving if a copy is needed. CSV export is provided; CSV import is not implemented. All bundled contacts are fictional and use `example.com` email addresses.

## Tests

```bash
python -m unittest discover -s tests -v
```

The suite covers empty trees, duplicates and normalized search, ordered traversal, deletion shapes, 1,500 randomized operations checked against a reference model, a 1,100-level skewed tree, benchmark correctness, and a Streamlit add/search/benchmark/delete workflow.

## Deployment

1. Push these files to a GitHub repository.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), select **Create app** and deploy from GitHub.
3. Select this repository, branch `main`, and entrypoint `app.py`.
4. Set Python to 3.12 in advanced settings and deploy.
5. Copy the working app URL into **Live application** above.

See the [official deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Files

- `app.py`: Streamlit interface and session state.
- `bst.py`: original BST data structure.
- `benchmark.py`: samples, linear search, and timing comparison.
- `requirements.txt`: pinned Streamlit dependency.
- `tests/`: automated structure, benchmark, and interface tests.
- `.streamlit/config.toml`: visual theme.

**Assignment numbering note:** This repository follows the requested Assignment 6.1 name. The campus page labels the same “Shipped application 2, Contact Directory” instructions as Module 6: Assignment 6.2. The implementation follows the Contact Directory instructions.
