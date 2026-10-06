import random
import unittest
from bst import Contact, ContactBST
from benchmark import compare, demo_tree, linear_search

class TreeTests(unittest.TestCase):
    def tree(self, names):
        tree = ContactBST()
        for name in names:
            tree.insert(Contact(name))
        return tree

    def test_empty(self):
        tree = ContactBST()
        self.assertIsNone(tree.search('Nobody'))
        self.assertFalse(tree.delete('Nobody'))
        self.assertEqual(list(tree.inorder()), [])
        self.assertEqual(tree.height(), 0)

    def test_normalization_duplicates_and_order(self):
        tree = self.tree(['Maria', 'Alice', 'Zoe', 'bob'])
        self.assertFalse(tree.insert(Contact('  ALICE  ')))
        self.assertEqual(tree.search(' alice ').name, 'Alice')
        self.assertEqual([c.name for c in tree.inorder()], ['Alice', 'bob', 'Maria', 'Zoe'])
        self.assertEqual(len(tree), 4)
        with self.assertRaises(ValueError):
            Contact('   ')

    def test_deletion_shapes(self):
        for names, target in [(['M'], 'M'), (['M', 'A'], 'M'), (['M', 'Z'], 'M'),
                              (['M', 'A', 'Z'], 'A'), (['M', 'A', 'Z'], 'M'),
                              (['M', 'A', 'Z', 'T', 'U'], 'M'), (['M', 'A', 'C'], 'A')]:
            with self.subTest(names=names):
                tree = self.tree(names)
                self.assertTrue(tree.delete(target))
                self.assertFalse(tree.delete(target))
                self.assertEqual([c.name for c in tree.inorder()], sorted(set(names) - {target}))
                self.assertEqual(len(tree), len(names) - 1)
                for name in set(names) - {target}:
                    self.assertIsNotNone(tree.search(name))

    def test_random_operations_against_reference(self):
        rng = random.Random(61)
        tree, expected = ContactBST(), {}
        for _ in range(1500):
            name = f'Person {rng.randrange(100):03d}'
            if rng.random() < .55:
                contact = Contact(name)
                self.assertEqual(tree.insert(contact), name not in expected)
                expected.setdefault(name, contact)
            else:
                self.assertEqual(tree.delete(name), name in expected)
                expected.pop(name, None)
            self.assertEqual(list(tree.inorder()), [expected[k] for k in sorted(expected)])
            self.assertEqual(len(tree), len(expected))
            self.assertEqual(tree.search(name), expected.get(name))

    def test_degenerate_tree_avoids_recursion_limit(self):
        tree = self.tree([f'{i:04d}' for i in range(1100)])
        self.assertEqual(tree.height(), 1100)
        self.assertEqual(len(list(tree.inorder())), 1100)
        self.assertTrue(tree.delete('1099'))

    def test_benchmark_same_data_and_no_mutation(self):
        tree = demo_tree(100)
        before = list(tree.inorder())
        self.assertEqual(tree.search(' CONTACT 00003 '), linear_search(before, ' CONTACT 00003 '))
        result = compare(tree)
        self.assertEqual(result['contacts'], 100)
        self.assertEqual(result['hits'], 100)
        self.assertEqual(result['queries'], 200)
        self.assertEqual(list(tree.inorder()), before)
        for samples in result['samples_ms'].values():
            self.assertEqual(len(samples), 5)
            self.assertTrue(all(t > 0 for t in samples))
        with self.assertRaises(ValueError):
            compare(ContactBST())
