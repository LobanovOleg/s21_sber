import asyncio
import random

from enum import Enum, auto
from random import choice


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


neo_reactions = {
    Action.HIGHBLOCK: Action.LOWKICK,
    Action.HIGHKICK: Action.HIGHBLOCK,
    Action.LOWBLOCK: Action.HIGHKICK,
    Action.LOWKICK: Action.LOWBLOCK,
}


class Agent:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        return choice(self.actions)

    async def fight(self):
        neo = Agent()
        self.__aiter__()
        neo.__aiter__()
        while self.health:
            agent_r = await self.__anext__()
            neo_r = neo_reactions[agent_r]
            if neo_r in (Action.LOWKICK, Action.HIGHKICK):
                self.health -= 1
            print(f"Agent: {agent_r}, Neo: {neo_r}, Agent Health: {self.health}")
        print("Neo wins!")


async def fightmany(n):
    agents = [Agent().__aiter__() for i in range(n)]
    neo = Agent()
    neo.__aiter__()
    while any(a.health for a in agents):
        alive = [a for a in agents if a.health > 0]
        if not alive:
            break
        agent = choice(alive)
        agent_r = await agent.__anext__()
        neo_r = neo_reactions[agent_r]
        if neo_r in (Action.LOWKICK, Action.HIGHKICK):
            agent.health -= 1
        print(
            f"Agent {agents.index(agent) + 1}: {agent_r}, Neo: {neo_r}, Agent {agents.index(agent) + 1} Health: {agent.health}"
        )
    print("Neo wins!")


if __name__ == "__main__":
    agent = Agent()
    asyncio.run(agent.fight())

    asyncio.run(fightmany(3))
