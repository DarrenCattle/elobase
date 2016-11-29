# elobase     
`python -i main.py`    
# Tech    
 - Python 3    
 - Sqlite 3 (for development)

# Architecture  

### Players

- id
- name
- Game_History ("tic")
- Game_History ("tac")
- Game_History ("toe")
- Summary Object
  - {(name, rating, wins, losses)}
  - {("tic", 1000, 12, 32), ("tac", 1100, 23, 32), ("toe", 1200, 32, 23)}

### Databases
  
- Player_DB (master table)
- Game_History_DB (could be individual or combined)
- Game_Players_DB ("tic")
- Game_History_DB 
- Game_Players_DB ("tac")
- Game_History_DB
- Game_Players_DB ("toe")
