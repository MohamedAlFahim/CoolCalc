from typing import List


class Signal:
    def __init__(self, content: str, targets: List[str]=None):
        self.content = content
        self.targets = targets

    def propagate_to_children(self, children, child_index=None):
        if child_index is None:  # Propagate to all children
            for child in children:
                if (self.targets is None) or (child.fits(self.targets)):
                    child.handle_signal(Signal(self.content, self.targets))
        else:
            if (self.targets is None) or (children[child_index].fits(self.targets)):
                children[child_index].handle_signal(Signal(self.content, self.targets))
