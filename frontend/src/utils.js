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

export function tomoveString(logm) {
  for (var i = 0; i < logm.length; i++) {
    if (i === 0){
      var movelog = ToSquare(logm[i])
    } else {
      movelog = movelog +'-'+ToSquare(logm[i]);
    }
  }
  return movelog;
}

export function getTurn(history_turn){
  let new_history=[];
  let item;
  const hist_length = history_turn.length;
  for (var i = 0; i < hist_length; i++){
    if ((i % 2) === 0){
      new_history.push({turn:i/2+1, human:history_turn[i].human, computer:" "});
    } else{
      item = new_history[new_history.length -1]
      item.computer= history_turn[i].human;
    }
  }
  return new_history;
}


export function legalMove(boardstate, id, visited, must_capture){

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
    if (((boardstate[next_move] === 'none') || (boardstate[next_move] === 'none eaten'))  && !(visited.includes(next_move))){
        if (must_capture){
            var len = visited.length;
            if (len >1){
                var last_selected = visited[len-2];
                last_id = visited[len-1];
                last_move = last_id - last_selected;    
            } else{
                last_move = 0;
                last_id = 0;
            }
            if ((can_capture(boardstate, id, valid_move[i])) && (valid_move[i] !== last_move)) {
                possible_move.push(next_move);
            }
        } else {
            possible_move.push(id+valid_move[i]);
        }
      }
    }
  return possible_move;
}

export function augment(Obj1, Obj2) {
  var prop;
  for (prop in Obj2){
    if (Obj2.hasOwnProperty(prop)){
      Obj1[prop] = Obj2[prop];
    }
  }
  return Obj1;
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


export function makeMove_choosen(boardstate, selected, newpos, i){
  var movetype = newpos - selected;
  var direction, pos_eat;
  boardstate = boardstate.map(function(item) { return item === 'none eaten' ? 'none' : item; });
  if ((selected + 2*movetype) === i){
    direction = movetype;
    pos_eat = newpos + direction;
  } else if ((selected - movetype) === i){
    direction = -movetype;
    pos_eat = newpos + 2*direction;
  }
  boardstate[selected] = 'none';
  boardstate[newpos] = 'one';
  while (boardstate[pos_eat] === 'two'){
      boardstate[pos_eat] = 'none eaten';
      pos_eat = pos_eat + direction;
  }
  return boardstate;
}



export function makeMove(boardstate, selected, newpos, movetype){
    var direction;
    var pos_eat;
    boardstate = boardstate.map(function(item) { return item === 'none eaten' ? 'none' : item; });
    if (boardstate[selected + 2*movetype] === 'two'){
        direction = movetype;
        pos_eat = newpos + direction;
    } else if (boardstate[selected - movetype] === 'two'){
        direction = -movetype;
        pos_eat = newpos + 2*direction;
    }
    boardstate[selected] = 'none';
    boardstate[newpos] = 'one';
    while (boardstate[pos_eat] === 'two'){
        boardstate[pos_eat] = 'none eaten';
        pos_eat = pos_eat + direction;
    }
    return boardstate;
  }
  

  export function MustCapture(boardstate, has_moved){
    var must_capture;
    if (has_moved){
      must_capture = true;
    } else {
      must_capture = has_capture(boardstate);
    }
    return must_capture;
  }


  export function is_winner(board){
    let my_pieces_count = 0;
    let opp_pieces_count = 0;
    for (var i = 0; i<50; i++){
      if (board[i] === 'one'){
        ++my_pieces_count;
      } else if (board[i] === 'two') {
        ++opp_pieces_count;
      }
    }
    if (my_pieces_count === 0){
      return 'Computer WIN';
    } else if (opp_pieces_count === 0){
      return 'You WIN';
    } else {
      return null;
    }
  }

  export  function get_board(gametype){
    let board;
    if (gametype === 'vakyloha'){
      board = ["none","one","one","one","one","none eaten","one","one","one","one",
        "none","one","one","one","one","none eaten","one","one","one","one",
        "none","two","one","two","one","two","two","one","two","one",
        "none","two","two","two","two","none","two","two","two","two",
        "none","two","two","two","two","two","two","two","two","two"];
    } else if (gametype === 'kobana') {
      board = [ "none","one","one","one","one","one","one","one","one","one",
      "none","one","one","one","one","one","one","one","one","one",
      "none","two","one","two","one","two","none","none eaten","two","one",
      "none","two","two","two","two","two","two","two","two","two",
      "none","two","two","two","two","two","two","two","two","two"
    ];
    } else if (gametype === 'fohy') {
      board = ["none","one","one","one","one","one","one","one","one","one",
      "none","one","one","one","one","one","one","one","one","one",
      "none","two","one","two","none eaten","two","none","one","two","one",
      "none","two","two","two","two","two","two","two","two","two",
      "none","two","two","two","two","two","two","two","two","two"
                ];
    } else if (gametype === 'havia') {
      board = [ "none","one","one","none eaten","one","one","one","one","one","one",
                "none","one","one","one","none eaten","one","one","one","one","one",
                "none","two","one","two","one","two","two","one","two","one",
                "none","two","two","two","two","two","none","two","two","two",
                "none","two","two","two","two","two","two","two","two","two"
                ];      
    } else if (gametype === 'havanana'){
      board = [ "none","one","one","one","one","one","one","none eaten","one","one",
                "none","one","one","one","one","one","none eaten","one","one","one",
                "none","two","one","two","one","two","two","one","two","one",
                "none","two","two","two","none","two","two","two","two","two",
                "none","two","two","two","two","two","two","two","two","two"
                ];      
    }
    return board;
  }

  export function getInitialState() {
    const initialState = {
      history: [{
        boardState: create_board(173538815, 562399469895680),
      }],
      selected: null,
      step_number: 0,
      has_moved: null,
      available_move: [],
      visited: [],
      must_choose: [],
      computer_move: false,
      is_moving: false,
      was_capture: false,
      status: null,
      depth:3,
      game_type:null,
      move_first:'human',
      winner: false,
      history_turn: [{
        boardState: create_board(173538815, 562399469895680),
        turn_id: 0,
        human:'',
        computer:'',
      }],
      turn_number: 0,
    };
    return initialState;
}
