from datetime import date


class StoryNode:
    def __init__(self, headline, content):
        self.headline = headline
        self.content = content
        self.next = None


class DiaryNode:
    def __init__(self, new_date: date, new_story: StoryNode):
        self.date = new_date
        self.stories = new_story
        self.prev = None
        self.next = None

    def append(self, new_story):
        last = self.stories
        while last.next:
            last = last.next
        last.next = new_story


class DiaryList:
    def __init__(self):
        self.head = None

    def sorted_insert(self, new_date: date, new_story: StoryNode):
        # Skip adding if data already exists in the list
        current = self.head
        while current:
            if current.date == new_date:
                current.append(new_story)
                return
            current = current.next

        new_node = DiaryNode(new_date, new_story)
        if self.head is None:  # If the list is empty
            self.head = new_node
            return

        # If new node should be the new head
        if self.head.date >= new_date:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            return

        current = self.head
        while current.next is not None and current.next.date < new_date:
            current = current.next

        # If new node should be the new tail
        new_node.next = current.next

        # If the new node is not inserted
        # at the end of the list
        if current.next is not None:
            new_node.next.prev = new_node

        current.next = new_node
        new_node.prev = current

    def append(self, new_diary):
        last = self.head
        new_diary.next = None
        if self.head is None:
            new_diary.prev = None
            self.head = new_diary
            return
        while last.next is not None:
            last = last.next
        last.next = new_diary
        new_diary.prev = last

    def to_list(self):
        current = self.head
        data = []
        while current:
            sub_data = [str(current.date)]
            stories = current.stories
            while stories:
                sub_data.append([stories.headline, stories.content])
                stories = stories.next
            data.append(sub_data)
            current = current.next
        return data

    def clear(self):
        self.head = None
