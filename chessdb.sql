
/*
* Create a table call history. This history has primary key idHistory 
* and a long text variable that keep track of the moves for a game.
*
* @ Columns:
* idHistory: Primary Key (auto-increment)
* MoveHistory: List of moves in history
* idUser: Foreign Key to User table
* idOpeningBook: Foreign Key to Opening Book table
* idEndgame: Foreign Key to Endgame table
*/
CREATE TABLE `history` (
  `idHistory` int NOT NULL AUTO_INCREMENT,
  `MoveHistory` longtext NOT NULL,
  `idUser` INT NOT NULL,
  `idOpeningBook` INT NOT NULL,
  `idEndgame` INT NOT NULL,
  PRIMARY KEY (`idHistory`),
  FOREIGN KEY (`idOpeningBook`) REFERENCES openingbook(`idOpeningBook`),
  FOREIGN KEY (`idUser`) REFERENCES user(`idUser`),
  FOREIGN KEY (`idEndgame`) REFERENCES endgame(`idEndgame`)
);

/*
* Create a table call 'engine'. Table 'engine' will assign a unique number
* to identify a user's game. This will allow us to keep track of the user's
* game and allow us to reference the game in the history table.
*
* @ Columns:
* idEngine: Primary key (auto-increment)
* EngineName: Name of the engine
* EngineCode: Code for the engine
* Username: username or alias for game
*/
CREATE TABLE `engine` (
  `idEngine` int NOT NULL AUTO_INCREMENT,
  `EngineName` varchar(50) NOT NULL,
  `EngineCode` varchar(50) NOT NULL,
  `Username` varchar(50),
  PRIMARY KEY (`idEngine`)
);

/*
* Create a table called 'openingbook'. This table records the opening
* moves of chess. This allows our chess engine to have a reference.
*
* @ Columns:
* idOpeningBook: Primary key (auto-increment)
* Name: Name of the opening move
* OpeningMove: Opening move in chess
* FullMove: Full position moves 
*/
CREATE TABLE `openingbook` (
  `idOpeningBook` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `OpeningMove` varchar(4) NOT NULL,
  `FullMove` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idOpeningBook`)
);

/*
* Create a table called 'endgame'. This table will record the endgame
* moves to simplify and develop chess moves for our chess engine during
* late game (where there is endless possibilities)
* 
* @ Columns:
* idEndgame: Primary Key
* EndgamePieces: Chess pieces that are left
* EndgamePosition: Endgame chess position
*/
CREATE TABLE `endgame` (
  `idEndgame` int NOT NULL AUTO_INCREMENT,
  `EndgamePieces` longtext NOT NULL,
  `EndgamePosition` longtext NOT NULL,
  PRIMARY KEY (`idEndgame`)
);


