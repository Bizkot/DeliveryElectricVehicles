class Node:
    def __init__(self, visit):
        self.data = visit
        self.next = None


class VisitLinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        return " -> ".join(": ".join((str(visit.visit_id), visit.visit_name)) for visit in nodes)

    def add_last(self, visit):
        new_node = Node(visit)
        if self.head is None:
            self.head = new_node
            return
        n = self.head
        while n.next is not None:
            n = n.next
        n.next = new_node
