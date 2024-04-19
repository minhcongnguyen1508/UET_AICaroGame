//TODO: Assign link of API here:
const api = 'http://localhost:1724/'

let game = {}
let roomId = undefined;
let fetchInterval;

document.getElementById("roomIdSubmit").addEventListener('click', handleSubmitRoomId)

function handleSubmitRoomId(){
    fetchInterval = setInterval(getJSON, 1000);
    const roomIdInput = document.getElementById("roomIdInput")
    roomId = roomIdInput.value;
}

function getJSON() {
    fetch(api)
        .then(response => response.json())
        .then(response => game = response)
        .catch(err => console.error(err));

    // let prevMatchId, currentMatchId 
    // currentMatchId = game.match_id
    if(game.status!= "None" && game.status!=undefined){
        // End the game
        console.log("Status: " + game.status)
        document.getElementById("status").style.display = "block";
        // document.getElementsByClassName("gameboard")[0].style.display = "none";
        document.getElementById("status").innerText = game.status;
        document.getElementById("confirm-button-container").style.display = "block";
        document.getElementById("confirm-button").addEventListener("click", handleConfirm);
        document.getElementById("roomid-input-container").style.display = "none";
        // prevMatchId = game.match_id
    }

    if(game.room_id===roomId && game.room_id !== undefined){
        drawBoard();   
        render();
    } 

}

function handleConfirm() {
    // Clear 
    game = {}
    clearInterval(fetchInterval);
    document.getElementById("status").style.display = "none";

    // Display room ID input
    document.getElementById("roomIdInput").value = "";
    document.getElementById("roomid-input-container").style.display="block";

    // Hide confirm button
    document.getElementById("confirm-button-container").style.display = "none";
}
var prevGameBoard;
function drawBoard() {
    document.getElementsByClassName("gameboard")[0].style.display = "block";
    document.getElementById("roomid-input-container").style.display="none";
    if (game.status == "None"){
        document.getElementById("status").style.display = "none";
        document.getElementById("confirm-button-container").style.display = "none";
    }
    
    var size = game.size;
    var gameBoard = document.getElementsByClassName("gameboard");
    var gameBoardHTML = "<table cell-spacing = '0'>";
    
    for (var i = 0; i < size; i++) {
        gameBoardHTML += "<tr>"
        for (var j = 0; j < size; j++) {
            if (prevGameBoard != undefined && game.board[i][j] == 'x' && prevGameBoard[i][j] === ' ') {
                gameBoardHTML += `<td style='width:${600 / size}px; height:${600 / size}px; font-size:${400 / size}px; font-weight: 300; color: rgb(254,96,93); background-color: rgba(238, 238, 238, 0.5); border: 3px solid rgb(254,96,93); border-collapse: collapse;'>`
                    + game.board[i][j]
                    + "</td>"
            }
            else if (prevGameBoard != undefined && game.board[i][j] == 'o' && prevGameBoard[i][j] === ' ') {
                gameBoardHTML += `<td style='width:${600 / size}px; height:${600 / size}px; font-size:${400 / size}px; font-weight: 300; color: #3DC4F3; background-color: rgba(238, 238, 238, 0.5); border: 3px solid #3DC4F3; border-collapse: collapse;'>`
                    + game.board[i][j]
                    + "</td>"
            }
                         
            else if (game.board[i][j] == 'x'){
                gameBoardHTML += `<td style='width:${600 / size}px; height:${600 / size}px; font-size:${400 / size}px; font-weight: 300; color: rgb(254,96,93)'>`
                + game.board[i][j]
                + "</td>"
            }
            else {
                gameBoardHTML += `<td style='width:${600 / size}px; height:${600 / size}px; font-size:${400 / size}px; font-weight: 300; color: #3DC4F3'>`
                + game.board[i][j]
                + "</td>"
            }

        }
        gameBoardHTML += "</tr>";
    }
    prevGameBoard = game.board;
    gameBoardHTML += "</table>";
    gameBoard[0].innerHTML = gameBoardHTML;

}

function render() {
    if (game.turn === game.team1_id) {
        document.getElementById('turn-flag-2').style.visibility = "hidden"
        document.getElementById('turn-flag-1').style.visibility = "visible"
    }
    else if (game.turn === game.team2_id) {
        document.getElementById('turn-flag-2').style.visibility = "visible"
        document.getElementById('turn-flag-1').style.visibility = "hidden"
    }
    else if (game.turn == undefined){
        document.getElementById('turn-flag-2').style.visibility = "hidden"
        document.getElementById('turn-flag-1').style.visibility = "hidden"
    }
    if (game.team1_id != undefined){
        let team1Parsed = game.team1_id.split("+");
        let teamId1 = team1Parsed[0].trim();
        let teamRole1 = team1Parsed[1].trim().toLowerCase();
        let avatarImg1 = document.querySelector(".player1-avatar img");
        if(teamRole1 == "x" || teamRole1 == "o"){
            avatarImg1.src = "resources/" + teamRole1 + "_role.png";
        }
        else {
            avatarImg1.src = "resources/player1avatar.png";
        }
        document.getElementById("player1-id").innerText = teamId1;
    }
    else {
        document.getElementById("player1-id").innerText = "";
        let avatarImg1 = document.querySelector(".player1-avatar img");
        avatarImg1.src = "resources/player1avatar.png";
    }

    if (game.team2_id != undefined){
        let team2Parsed = game.team2_id.split("+");
        let teamId2 = team2Parsed[0].trim();
        let teamRole2 = team2Parsed[1].trim().toLowerCase();
        let avatarImg2 = document.querySelector(".player2-avatar img");
        if(teamRole2 == "x" || teamRole2 == "o"){
            avatarImg2.src = "resources/" + teamRole2 + "_role.png";
        }
        else {
            avatarImg2.src = "resources/player2avatar.png";
        }
        document.getElementById("player2-id").innerText = teamId2;
      }
      else {
        document.getElementById("player2-id").innerText = "";
        let avatarImg2 = document.querySelector(".player2-avatar img");
        avatarImg2.src = "resources/player2avatar.png";
      }
    document.getElementById("match-id").innerText = `Match ID: ${game.match_id != undefined ? game.match_id : ""}`
    document.getElementById('player1-time').innerHTML = game.time1 != undefined ? game.time1.toFixed(5) : ""
    document.getElementById('player2-time').innerHTML = game.time2 != undefined ? game.time2.toFixed(5) : ""
    document.getElementById('score1').innerHTML = game.score1 != undefined ? game.score1 : ""
    document.getElementById('score2').innerHTML = game.score2 != undefined ? game.score2 : ""

}






