"""An original, iterative binary search tree. Author: Juan Pablo Osorio."""
from dataclasses import dataclass
from typing import Iterator


def normalize(name: str) -> str:
    return " ".join(name.split()).casefold()


@dataclass(frozen=True)
class Contact:
    name: str
    phone: str = ""
    email: str = ""

    def __post_init__(self):
        object.__setattr__(self, "name", " ".join(self.name.split()))
        object.__setattr__(self, "phone", self.phone.strip())
        object.__setattr__(self, "email", self.email.strip())
        if not self.name:
            raise ValueError("A contact name is required.")

    @property
    def key(self) -> str:
        return normalize(self.name)


@dataclass
class Node:
    contact: Contact
    left: "Node | None" = None
    right: "Node | None" = None


class ContactBST:
    """Unique normalized names; no library tree or dictionary backs storage."""

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def insert(self, contact: Contact) -> bool:
        """Return False for a duplicate, preserving the existing contact."""
        if self.root is None:
            self.root = Node(contact)
            self.size += 1
            return True
        current = self.root
        while True:
            if contact.key == current.contact.key:
                return False
            side = "left" if contact.key < current.contact.key else "right"
            child = getattr(current, side)
            if child is None:
                setattr(current, side, Node(contact))
                self.size += 1
                return True
            current = child

    def search(self, name: str) -> Contact | None:
        key = normalize(name)
        current = self.root
        while current is not None:
            if key == current.contact.key:
                return current.contact
            current = current.left if key < current.contact.key else current.right
        return None

    def inorder(self) -> Iterator[Contact]:
        """Left, node, right traversal; no sorting function is used."""
        stack = []
        current = self.root
        while stack or current is not None:
            while current is not None:
                stack.append(current)
                current = current.left
            current = stack.pop()
            yield current.contact
            current = current.right

    def delete(self, name: str) -> bool:
        key = normalize(name)
        parent = None
        current = self.root
        while current is not None and current.contact.key != key:
            parent = current
            current = current.left if key < current.contact.key else current.right
        if current is None:
            return False
        # Two children: replace with the inorder successor, then remove it.
        if current.left is not None and current.right is not None:
            successor_parent = current
            successor = current.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            current.contact = successor.contact
            parent, current = successor_parent, successor
        child = current.left if current.left is not None else current.right
        if parent is None:
            self.root = child
        elif parent.left is current:
            parent.left = child
        else:
            parent.right = child
        self.size -= 1
        return True

    def height(self) -> int:
        """Height in levels: empty=0, root only=1."""
        if self.root is None:
            return 0
        pending = [(self.root, 1)]
        result = 0
        while pending:
            node, depth = pending.pop()
            result = max(result, depth)
            if node.left is not None:
                pending.append((node.left, depth + 1))
            if node.right is not None:
                pending.append((node.right, depth + 1))
        return result
