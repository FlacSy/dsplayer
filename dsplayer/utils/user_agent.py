import random

def get_random_user_agent() -> str:
    with open("dsplayer/utils/local/user_agents.txt", "r", encoding="utf-8") as file:
        user_agents = file.readlines()
        user_agent = random.choice(user_agents)
        return user_agent.replace("\n", "")