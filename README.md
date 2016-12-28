# elobase     
`python -i main.py` 
`python index.py`
# Tech    
 - Python 3    
 - Sqlite 3 (for development)

# Architecture  

### Player
- id
- name
    
### Game
- id
- name
    
### Instance
- id
- created
- game_id
- winner_id
- loser_id

### Result
- id
- created
- game_id
- instance_id
- player_id
- elo

### Instance_Multi
- in development
