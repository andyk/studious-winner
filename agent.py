import time
import random
import threading


class Agent:
    def __init__(self, agent_id, env):
        self.conscious = ConsciousThoughtUnit(agent_id)
        self.validation = SocialValidationUnit(agent_id)
        self.agent_id = agent_id
        self.env = env

    def start(self):
        self.conscious.start()
        self.validation.start()


class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority
        self.activity = None

    def execute(self):
        print(f"{self.name} is {self.activity}...")


class ThinkHardTask(Task):
    def __init__(self, name, priority):
        super().__init__(name, priority)
        self.activity = "thinking hard"


class SayNameTask(Task):
    def __init__(self, name, priority):
        super().__init__(name, priority)
        self.activity = "talking"


class Unit(threading.Thread):
    def __init__(self):
        super().__init__()
        self.task_pool = []

    def run(self):
        self.task_pool = sorted(self.task_pool, key=lambda x: x.priority)
        while True:
            self.task_pool[0].execute()
            denom = random.choice(range(1, 40))
            time.sleep(1 / denom)


class ConsciousThoughtUnit(Unit):
    def __init__(self, agent_id):
        super().__init__()
        self.name = f"Conscious Thought Unit for Agent {agent_id}"
        self.think_task = ThinkHardTask(self.name, 101)
        self.say_task = SayNameTask(self.name, 100)
        self.task_pool.append(self.think_task)
        self.task_pool.append(self.say_task)


class SocialValidationUnit(Unit):
    def __init__(self, agent_id):
        super().__init__()
        self.name = f"Social Validation Unit for Agent {agent_id}"
        self.think_task = ThinkHardTask(self.name, 100)
        self.say_task = SayNameTask(self.name, 101)
        self.task_pool.append(self.think_task)
        self.task_pool.append(self.say_task)


if __name__ == "__main__":
    a1 = Agent("agent 1", {})
    # a2 = Agent('agent 2', {})
    a1.start()
    # a2.start()
