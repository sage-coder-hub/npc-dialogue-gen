import ollama
import random
NPC={"name":"Deputy Welles","role":"Freestar ranger","personality":"Stoic, observant, slow to trust, deeply principled",
     "location":"Akila city checkpoint","backstory":"Veteran ranger, seen too many outlaws walkl free on technicalities.",
     "quirks":"Keeps one hand near his holster when strangers approach","injuries":"Old laser burn on his neck, never talks about it"}
PLAYER_STATE={"name":"Sarah","reputation":"Feared in outer systems","last_action":"Just docked from a raid but wiped the evidence",
              "equipped":"modified Magshear, bloodied jacket","bounty":"none currently, warrents paid off somehow",
              "affiliation":"Crimson Fleet adjacent, no formal ties on record","health":"full"}
def dict_to_context(d:dict) -> str:
    return "\n".join(f"-{key.replace('_',' ')}: {value}" for key,value in d.items())
def build_prompt(npc:dict,player:dict,pool_size:int=20) -> str:
    return f"""You are generating ambient dialogue for an RPG game.
    You are the NPC, role play as: {dict_to_context(NPC)}
    Player context: {dict_to_context(PLAYER_STATE)}
    Write ONE line the npc mutters to themselves while going on about their work.
    Rules:
    - One single line only, no more
    - Under 10 words
    - No questions
    - No "you" or addressing anyone
    - No preamble, explanation, or quotation marks
    - Just the line itself, nothing else
    - Can refrence the player state or actions, but not directly address them by name
    - Role play as the npc, not as a narrator and immersed in the world"""
def parse_lines(raw:str) -> list[str]:
    lines=[]
    for line in raw.splitlines():
        line=line.strip()
        if not line:
            continue
        if line[0].isdigit() and line[1] in ".):-":
            line=line[2:].strip()
        if len(line.split())>12:
            continue
        lines.append(line)
    return lines
def generate_one(npc:dict,player:dict) -> str:
    #print("Generating line...")
    response=ollama.chat(model="qwen2.5:1.5b",messages=[{"role":"user","content":build_prompt(npc,player)}])
    #print("Got response, parsing...")
    line=response["message"]["content"].strip()
    line=line.strip('"').strip("'").strip()
    if "\n" in line or len(line.split())>12:
        return None
    return line
def generate_pool(npc:dict,player:dict,pool_size:int=20) -> list[str]:
    #print(f"Generating {pool_size} dialogue lines for {npc['name']}...")
    pool=[]
    attempts=0
    while len(pool)<pool_size and attempts<pool_size*2:
        attempts+=1
        line=generate_one(npc,player)
        if line:
            pool.append(line)
            print(f"[{len(pool):02}/{pool_size}] {line}")
    print()
    return pool
def simulate_encounter(pool:list[str],num_lines:int=5):
    print(f"===Player approaches {NPC['name']}===\n")
    sample=random.sample(pool,min(num_lines,len(pool)))
    for line in sample:
        print(f'{NPC["name"]}: "{line}"')
if __name__=="__main__":
    pool=generate_pool(NPC,PLAYER_STATE,pool_size=20)
    print(f"Pool ready - {len(pool)} lines\n")
    print()
    simulate_encounter(pool,num_lines=5)
    print("\n--- Player reloads save and approaches again ---\n")
    simulate_encounter(pool,num_lines=5)