class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score= 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score += 1
        else:
            self.player2_score += 1

    def even_score(self, score):
        scores = ["Love-All", "Fifteen-All", "Thirty-All"]
        if score > 2:
            return "Deuce"
        else:
            return scores[score]
        
    def uneven_score(self, difference):
        if difference == 1:
            return "Advantage player1"
        elif difference == -1:
            return "Advantage player2"
        elif difference >= 2:
            return "Win for player1"
        else:
            return "Win for player2"
        
    def uneven_low_score(self, score1, score2):
        scores = ["Love", "Fifteen", "Thirty", "Forty"]
        return scores[score1] + "-" + scores[score2]

    def get_score(self):
        if self.player1_score == self.player2_score:
            score = self.even_score(self.player1_score)

        elif self.player1_score >= 4 or self.player2_score >= 4:
            difference = self.player1_score - self.player2_score
            score = self.uneven_score(difference)

        else:
            score = self.uneven_low_score(self.player1_score, self.player2_score)

        return score
