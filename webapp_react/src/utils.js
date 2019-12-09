export function create_board(my_pieces, opp_pieces){
    var stones = Array(50).fill('none');
    var my_pieces_binrepr = (my_pieces).toString(2).padStart(64,'0');
    var opp_pieces_binrepr = (opp_pieces).toString(2).padStart(64,'0');
    var my_len = my_pieces_binrepr.length;
    var opp_len = opp_pieces_binrepr.length;  
    for (var i = 0; i < 50; i++) {
      if (my_pieces_binrepr.charAt(my_len - i) === '1'){
        stones[i] = 'one';
      } else if (opp_pieces_binrepr.charAt(opp_len -i) === '1'){
        stones[i] = 'two';
      } else {
        stones[i] = 'none';
      }
   }
   return stones
  }
  


export function ToSquare(id) {
    var column = 10 - (id % 10);
    var row = ~~(id / 10);
    var lookup = { "0":"e", "1":"d", "2":"c","3":"b", "4":"a"};
    return lookup[row]+column;
}


export function legalMove(boardstate, id, visited, hascapture, hasmoved){

  //const diagonal = 375116358920533;
  var possible_move =[];
  var valid_move;
  var last_move, last_id;
  if ((id % 2) !== ((~~(id / 10)) % 2)) {
    valid_move = [-11, -10, -9, -1, 1, 9, 10, 11];
  } else{
    valid_move = [-10, -1, 1, 10];
  }
  for (var i=0; i<valid_move.length; i++){
    var next_move = id + valid_move[i];
    if ((next_move % 10) === 0) {
        continue;
    }
    if ((boardstate[next_move] === 'none')  && !(visited.includes(next_move))){
        if (hascapture){
            var len = visited.length;
            if (len >1){
                var last_selected = visited[len-2];
                last_id = visited[len-1];
                last_move = last_id - last_selected;    
            } else{
                last_move = 0;
                last_id = 0;
            }
            if ((can_capture(boardstate, id, valid_move[i])) && (id !== (last_id + last_move))) {
                possible_move.push(id+valid_move[i]);
            }
        } else {
            possible_move.push(id+valid_move[i]);
        }
      }
    }
  return possible_move;
}

export function can_capture(boardstate, id, movetype){
    return ((boardstate[id + 2*movetype] === 'two') || (boardstate[id - movetype] === 'two'))
}

export function has_capture(boardstate){
    const my_pieces_idx = boardstate.reduce((a, e, i) => (e === 'one') ? a.concat(i) : a, []);
    var pmove;
    var visited = [];
    var hascapture = true;
    for (var i=0; i<my_pieces_idx.length; i++){
        pmove = legalMove(boardstate, my_pieces_idx[i], visited, hascapture);
        if (pmove.length >=1){
            return true;
        }
    }
    return false;
}

export function makeMove(boardstate, selected, newpos, movetype){
    var direction;
    var pos_eat;
    if (boardstate[newpos] === 'two'){
      // was must choose
      if ((selected + 2*movetype) === newpos){
          direction = movetype;
      } else if ((selected - movetype) === newpos){
          direction = -movetype;
      }
    } else{
        if (boardstate[selected + 2*movetype] === 'two'){
            direction = movetype;
            pos_eat = newpos + direction;
        } else if (boardstate[selected - movetype] === 'two'){
            direction = -movetype;
            pos_eat = newpos + 2*direction;
        } else{
            boardstate[selected] = 'none';
            boardstate[newpos] = 'one';
            return boardstate;
        }
      }
    while (boardstate[pos_eat] === 'two'){
        boardstate[pos_eat] = 'none';
        pos_eat = pos_eat + direction;
    }
    boardstate[selected] = 'none';
    boardstate[newpos] = 'one';
   
    return boardstate;
  }
  
  
  /* function board_tobit(boardstate){
    var my_pieces = 0;
    var opp_pieces = 0;
    var piece;
    for (var i = 0; i < 50; i++) {
      piece = boardstate[i];
      if (piece === "one"){
        my_pieces = my_pieces + (1<<i);
      } else if (piece === "two"){
        opp_pieces = opp_pieces + (1<<i);
      }
    }
    return [my_pieces.toString(2), opp_pieces.toString(2)];
  } */
  

