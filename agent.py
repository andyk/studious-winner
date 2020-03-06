import time
import random
import threading


class Agent:
    def __init__(self, agent_id, world):
        self.conscious = ConsciousThoughtUnit(agent_id)
        self.hunger = HungerDrive(self.conscious, world)
        self.agent_id = agent_id
        self.world = world

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
            time.sleep(1 / 40)


class ConsciousThoughtUnit(Unit):
    def __init__(self, agent_id):
        super().__init__()
        self.name = f"Conscious Thought Unit for Agent {agent_id}"
        self.thinking_task = ThinkHardTask(100)
        self.task_pool.append(self.thinking_task)


class HungerDrive(threading.Thread):
    def __init__(self, conscious, world):
        super().__init__()
        self.base_priority = 100
        self.conscious = conscious
        self.world = world
        self.eat_task = EatTask(self.base_priority, self.world)
        self.conscious.task_pool.append(self.eat_task)

    def run(self):
        while True:
            hunger_level = self.world.sense()
            next_priority = self.base_priority - hunger_level
            self.eat_task.priority = next_priority
            time.sleep(1 / 40)


class WorldOutsideOfConsciousThought:
    def __init__(self):
        self.amount_of_food = 100  # external apples avaiable
        self.agent_hunger = 0  # body sense of the agent

    def sense(self):
        hunger_up = random.choice([0, 1])  # TODO - separate running process
        self.agent_hunger += hunger_up
        print(f"hunger is now {self.agent_hunger}")
        return self.agent_hunger

    def eat(self, name):
        food_eaten = random.choice([0, 1, 2, 3])
        if self.amount_of_food < food_eaten:
            return
        print(f"{name} is eating {food_eaten} apples")
        self.amount_of_food -= food_eaten
        self.agent_hunger -= food_eaten


if __name__ == "__main__":
    world = WorldOutsideOfConsciousThought()
    a1 = Agent("agent 1", world)
    a1.start()
