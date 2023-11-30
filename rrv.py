import pandas

# read csv
data = pandas.read_csv('game_2023 Winter.csv')
data = data.fillna(0)
data = data[data['Waived'] != True]
data = data.transpose()

# Convert the DataFrame to a Dictionary
data_dicts = data.to_dict(orient='records')
games_name = data_dicts[0]
ballots = data_dicts[1:-4]
cost_dict = data_dicts[-4]

# parameters
seats = len(games_name)
seated = []
final_decision = []
cost = 0
count = 5
budget = 1000
max_score = max(max(ballot.values()) for ballot in ballots)

#reweight
def reweight(ballot):
  seated_scores = [
      ballot[candidate] for candidate in ballot if candidate in seated
  ]
  weight = 1/(1+sum(seated_scores)/max_score)
  return {candidate: weight*ballot[candidate] for candidate in ballot}

def nextRound(ballots):
  reweightedBallots = [reweight(ballot) for ballot in ballots]
  winner = pandas.DataFrame(reweightedBallots).sum().drop(seated).idxmax()
  seated.append(winner)
  return reweightedBallots

while len(seated) < seats:
  nextRound(ballots)

for i in range(count):
  new_game = seated[i]
  cost += cost_dict[new_game]
  if cost > budget:
    break
  final_decision.append(games_name[new_game])

print(final_decision)