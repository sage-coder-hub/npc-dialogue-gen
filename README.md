# npc-dialogue-gen
Lightweight local llm-powered ambient npc dialogue generator. Feed it a character dict, get a pool of contextual idle lines-no api costs, runs offline via Ollama.
Prerequisites-install Ollama from ollama.com and run "ollama pull qwen2.5:1.5b"
Install deps-"pip install -r requirements.txt"
How to run- python "NpcDioSheet.py"
How to customize-there is a NPC and PLAYER_STATS dict at the top of the program, the program should be able to plug and play any npc stats.
the llm prompt will automatically plug them in and run as the npc.

The llm model can be changed however the prompt may also need to be adjusted.
This is my first github upload so hope people enjoy.
