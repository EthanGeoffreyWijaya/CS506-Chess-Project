var username = "Guest" //"FoggierApollo"
var userTurn = 1 // White is 1 - Black is 2
var board = null;
var gameOver = true;
var random = false;
var playingModeHandlerAdded = false;

function makeMove(moveStr) {
    var moveFrom = moveStr.slice(0, 2);
    var moveTo = moveStr.slice(2, 4);
    var movePromotion = moveStr.length == 5 ? moveStr.slice(4, 5) : null;
    var move = {from: moveFrom, to: moveTo}
    board.game.move({
        ...move,
        promotion: movePromotion,
        animate: false,
        userGenerated: true
      });
}

function getPreviousMove() {
    // Get previous move
    previous_move_obj = board.game.getLastMove();
    // Check if there wasn't a previous move (first move)
    if (previous_move_obj == undefined) {
        return null;
    }
    // Get move string from previous move
    previous_move = previous_move_obj.from + previous_move_obj.to;
    if (previous_move_obj.promotion) {
        previous_move += previous_move_obj.promotion;
    }
    return previous_move;
}

function getRandomNextMove() {
    // Get next move
    possible_moves = board.game.getLegalMoves();
    // Get random move out of legal moves
    random_move = possible_moves[Math.floor(Math.random() * possible_moves.length)];
    // Get move string from random move
    next_move = random_move.from + random_move.to;
    if (random_move.promotion) {
        next_move += random_move.promotion;
    }
    return new Promise((resolve) => {setTimeout(function () { resolve(next_move); }, 3000)});
}

function getNextMove(previous_move, fen_str=null) {
    // Check if no previous moves (first move)
    if (previous_move == null) {
        console.log("First Move");
    }
    // Get next move
    const url = new URL('http://localhost:8080');
    const params =  fen_str != null ? 
                        new URLSearchParams({ fen_str: fen_str}) : 
                        (previous_move != null ?
                            new URLSearchParams({ prev_move: previous_move }) :
                            new URLSearchParams());
    return new Promise((resolve) => {
        fetch(url + params).then(
            function(response) {
                return response;
            }
        ).then(
            function(response) {
                // response is full response object
                console.log(response);
                // response.test() is the next move string
                resolve(response.text())
            }
        );
        // ).catch(
        //     function(err) {
        //         console.log('Fetch Error :-S', err);
        //     }
        // );
        });
    
}

function onMove(event) {
    // Check if game is over
    if (board.game.isGameOver() === true) {
        console.log("Game Over");
        gameOver = true;
        // Check who won
        // 1-0 is white won, 0-1 is black won, 1/2-1/2 is draw
        var result = board.game.getResult();
        // 1 is white, 2 is black, 0 is draw (based off turn number)
        var winner = result === "1-0" ? 1 : (result === "0-1" ? 2 : 0);
        if (winner === userTurn) {
            console.log("User Won");
        } else if (winner === 0) {
            console.log("Draw");
        } else {
            console.log("User Lost");
        }
         // Add gameStarted event listener (for detecting when starting new game)
         // Checks when mode is playing and selection screens aren't up
        if (playingModeHandlerAdded === false) {
            board.game.on("ModeChanged", playingModeHandler);
            playingModeHandlerAdded = true;
        }
    } else {
        var include_fen_str = false;
        // Game is not over
        // Check if it's the user's turn
        if (board.game.getTurn() == userTurn) {
            // If game was over (or initial move) then tell server to reset board to fen string
            if (gameOver === true) {
                gameOver = false;
                include_fen_str = true;
            }

            // Get previous move
            previous_move = getPreviousMove(board);
            console.log("Previous Move: " + previous_move);
            
            // If no previous move and not including fen string then don't get next move
            // Accidental repeat call due to event listener not controlled by me
            if (previous_move == null && include_fen_str === false) {
                return;
            }

            // Get next move then make the move
            next_move_func = random ? 
                             getRandomNextMove() : 
                             getNextMove(previous_move, include_fen_str ? board.game.getFEN() : null);
            
            next_move_func.then(function (next_move) {
                console.log("Next Move: " + next_move);
                makeMove(next_move);
            });
        }
    }
}

function newGame() {
    console.log("New Game");
    // Get team color for the game
    getUserTeam();
    // Start moving
    onMove();
}

function playingModeHandler() {
    // Check if game is not over and selection screens are not up
    // Wait for selection screens to change because sometimes they take a little
    setTimeout(function() {
        selection_screens = document.querySelector(".selection-menu-component, .selection-component");
        // console.log("Selection Screens: " + selection_screens);
        if (board.game.isGameOver() === false && selection_screens === null) {
            // Remove gameStarted event listener
            board.game.off({type: "ModeChanged", handler: playingModeHandler});
            playingModeHandlerAdded = false;
            // Start game
            newGame();
        }
    }, 100);
}

function getUserTeam() {
    // Get team color
    bottom_name = document.querySelector('#player-bottom').querySelector('.user-tagline-username').innerText;
    flipped = board.game.getOptions().flipped;
    // console.log("Bottom Name: " + bottom_name);
    // console.log("Flipped: " + flipped);
    // console.log("Username: " + username);
    if ((bottom_name === username && flipped === false) || (bottom_name !== username && flipped === true)) {
        console.log("User Team is White");
        userTurn = 1; // White
    } else {
        console.log("User Team is Black");
        userTurn = 2; // Black
    }
}

function reconnectToRestartedServer() {
    gameOver = true;
    onMove();
}

function init() {
    // Get board
    board = document.querySelector('.board');
    // Get if random moves or not
    var input = null;
    while (input !== "y" && input !== "n" && input !== "") {
        input = prompt("Random Moves? (y/n) - Default is n (Minimax Best Moves)");
    }
    // Add onMove event listener
    board.game.on("Move", onMove);
    // If game is setup it is not showing the selection screens
    if (document.querySelector(".selection-menu-component, .selection-component") === null) {
        // Start game
        newGame();
    } else {
        // Add gameStarted event listener (for detecting when starting new game)
        // Checks when mode is playing and selection screens aren't up
        if (playingModeHandlerAdded === false) {
            board.game.on("ModeChanged", playingModeHandler);
            playingModeHandlerAdded = true;
        }
    }
}

init();

// For getting evaluation bar score
// y = document.querySelector("wc-evaluation-bar")
// y.scoreHoverElement.innerHTML

// For getting useful information including WLD percentages
// Just for openings though
// board.game.eco
