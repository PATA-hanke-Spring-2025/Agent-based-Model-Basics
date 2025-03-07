## Your data mast be in two files ##
File for states:

| ID | State       |
|----|-------------|
| 1	 | PROSPECTING |
| 2	 | QUALIFYING  |
| 3	 | PROPOSING   |
| 4	 | NEGOTIATING |
| 5  | CLOSING     |
| 6  | MAINTAINING |


File for matrix (headers names and values can be different)

| From/To	  | PROSPECTING	| QUALIFYING | PROPOSING | NEGOTIATING | CLOSING | MAINTAINING |
|-------------|-------------|------------|-----------|-------------|---------|-------------|
| PROSPECTING | 0.6	        | 0.4	     | 0         | 0           | 0       | 	0          | 
| QUALIFYING  | 0	        | 0.6	     | 0.4       | 0           | 0       | 	0          |
| PROPOSING	  | 0	        | 0.1	     | 0.3       | 0.4         | 0.2     | 	0          |
| NEGOTIATING | 0	        | 0	         | 0.2       | 0.5         | 0.3     | 	0          |
| CLOSING     | 0	        | 0	         | 0         | 0.1         | 0.2     | 	0.5        |
| MAINTAINING | 0	        | 0		     | 0         | 0           | 0.3     | 	0.7        |


but the number of states and their names in the sates file must be the same in the matrix file. 