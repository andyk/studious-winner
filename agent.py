import time
import random
import threading
from multiprocessing import Process, Value


BRAIN_TICK = 1
WORLD_TICK = 1


class Agent:
    def __init__(self, agent_id, world):
        self.world = world
        self.agent_id = agent_id
        self.conscious = ConsciousThoughtUnit(self.agent_id)
        self.hunger = HungerDrive(self.conscious, self.world)

    def start(self):
        self.conscious.start()
        self.hunger.start()


class Task:
    def __init__(self, activity, priority):
        self.activity = activity
        self.priority = priority

    def execute(self, name):
        print(f"{name} is {self.activity} (priority: {self.priority})...")


class ThinkHardTask(Task):
    def __init__(self, priority):
        super().__init__("thinking", priority)


class EatTask(Task):
    def __init__(self, priority, world):
        super().__init__("eating", priority)
        self.world = world

    def execute(self, name):
        self.world.eat(name)


class Unit(threading.Thread):
    def __init__(self):
        super().__init__()
        self.task_pool = []

    def run(self):
        while True:
            self.task_pool = sorted(self.task_pool, key=lambda x: x.priority)
            self.task_pool[0].execute(self.name)
            time.sleep(BRAIN_TICK)


class ConsciousThoughtUnit(Unit):
    def __init__(self, agent_id):
        super().__init__()
        self.name = f"Conscious Thought Unit for Agent {agent_id}"
        self.thinking_task = ThinkHardTask(100)
        self.task_pool.append(self.thinking_task)


class HungerDrive(threading.Thread):
    def __init__(self, conscious, world):
        super().__init__()
        self.base_priority = 101
        self.conscious = conscious
        self.world = world
        self.eat_task = EatTask(self.base_priority, self.world)
        self.conscious.task_pool.append(self.eat_task)

    def run(self):
        while True:
            hunger_level = self.world.hunger.value
            next_priority = self.base_priority - hunger_level
            self.eat_task.priority = next_priority
            time.sleep(BRAIN_TICK)


class WorldOutsideOfConsciousThought:
    def __init__(self):
        self.hunger = Value("i", 0)
        self.apple_count = Value("i", 100)
        self.process = Process(target=self.simulate)

    def start(self):
        self.process.start()

    def simulate(self):
        while True:
            print(f"Agent is getting hungrier: {self.hunger.value}")
            self.hunger.value += 1
            time.sleep(WORLD_TICK)

    def sense(self):
        print(f"Agent is sensing hunger as {self.hunger.value}")
        return self.hunger.value

    def eat(self, name):
        food_eaten = random.choice([0, 1, 2, 3])
        if self.apple_count.value < food_eaten:
            return
        self.apple_count.value -= food_eaten
        self.hunger.value -= food_eaten
        print(
            f"{name} is eating {food_eaten} apples, "
            f"{self.apple_count.value} apples left"
        )


if __name__ == "__main__":
    world = WorldOutsideOfConsciousThought()
    world.start()
    agent = Agent("Agent 1", world)
    agent.start()
