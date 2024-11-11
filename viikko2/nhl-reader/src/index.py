from player import PlayerReader, PlayerStats
from rich.console import Console
from rich.table import Table

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2023-24/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    season = input("Select season [2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/]")

    while True:
        nationality = input("Select nationality [AUT/CZE/AUS/SWE/GER/DEN/SUI/SVK/NOR/RUS/CAN/LAT/BLR/SLO/USA/FIN/GBR]")
        table = Table(title=f"Top scorers of {nationality} season {season}")

        players = stats.top_scorers_by_nationality(nationality)


        table.add_column("name", justify="right", style="cyan", no_wrap=True)
        table.add_column("team", justify="right", style="magenta")
        table.add_column("goals", justify="right", style="green")
        table.add_column("assists", justify="right", style="green")
        table.add_column("points", justify="right", style="green")

        for player in players:
            table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.goals + player.assists))

        console = Console()
        console.print(table)

if __name__ == "__main__":
    main()
