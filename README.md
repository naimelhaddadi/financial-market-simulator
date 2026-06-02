FINAL PROJECT: FINANCIAL MARKET SIMULATOR (CONSOLE)
General Description
The goal of this project is to create a turn-based financial strategy game that runs in the VS Code terminal. The user will take on the role of an investor managing a starting capital of $10,000 across 12 months (turns).

In-game time is frozen: each month is a phase where the user can execute as many buy and sell transactions as their funds allow. The market and asset prices will only change when the user explicitly chooses to end their turn.

Game Loop Structure
The program will be structured using two nested loops: a main loop that controls the progression of the months, and an internal secondary loop that processes the player's decisions within the current month.

Phase 1: Start of the Month (Automatic and Frozen)
At the beginning of each of the 12 months, the program will automatically execute the following actions only once:

Price Fluctuations: Modify asset prices using the random library (e.g., a random variation between -5% and +5%). The starting assets will be: Apple (AAPL) ($150), Tesla (TSLA) ($100), and Bitcoin (BTC) ($500).

Event of the Month: Select a random news headline from a predefined list and apply an extra percentage impact to the affected company.

Market Locking: The resulting prices will freeze and will not change for the remainder of that month.

Phase 2: Player's Trading Turn (Decision Loop)
The program will print the console interface showing the current state (Month, Cash, fixed prices for the month, and owned shares) and will enter a continuous input() loop awaiting user commands.

The user will be able to execute multiple commands in a row during the same month:

buy [ASSET] [AMOUNT]: Reduces cash, increases owned shares, and redisplays the interface for the same month with the same prices to allow further transactions.

sell [ASSET] [AMOUNT]: Increases cash, reduces owned shares, and redisplays the interface for the same month.

next / pass: Breaks the internal decision loop, allows the program to advance to the next month (+1 to the month counter), and restarts Phase 1 with new prices.

Technical Requirements and Error Handling
To ensure the project is robust and high-level, the code must prevent the user from breaking the game:

Funds Validation: If the user attempts to buy shares for a value higher than their available cash, the program will display an "Insufficient funds" warning, ignore the command, and request a new input for the same month.

Inventory Validation: If they attempt to sell more shares than they actually own of a specific asset, the program will display an "Insufficient shares" error.

Command Validation: If the user makes a typo (e.g., misspells a command or an asset name), the program must cleanly notify the user without closing or crashing, and prompt for the command again.

End of Game and Evaluation
Once month 12 is completed and the user inputs the pass/next command, the game will end and display the final summary screen:

It will calculate the Total Net Worth by adding the remaining cash to the total value of the owned shares, valued at the closing prices of month 12.

It will display a detailed breakdown of their performance along with a personalized message based on whether they managed to beat the initial $10,000 or ended up with a loss.
