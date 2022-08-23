export function create_board(my_pieces, opp_pieces){
    let stones = Array(50).fill('zero');
    let my_pieces_binrepr = (my_pieces).toString(2).padStart(64,'0');
    let opp_pieces_binrepr = (opp_pieces).toString(2).padStart(64,'0');
    let my_len = my_pieces_binrepr.length;
    let opp_len = opp_pieces_binrepr.length;  
    for (let i = 0; i < 50; i++) {
      if (my_pieces_binrepr.charAt(my_len - i) === '1'){
        stones[i] = 'one';
      } else if (opp_pieces_binrepr.charAt(opp_len -i) === '1'){
        stones[i] = 'two';
      }
   }
   return stones
  }


export function was_capture(prev, curr) {
  const [my, opp] = count_pieces(curr)
  const [my_prev, opp_prev] = count_pieces(prev)
  if ((my < my_prev) || (opp < opp_prev)){
    return true
  }
  return false
}


export function get_first_move(board, move_string){
  let game_type;
  switch(move_string){
    case 'd5-c5':
      game_type = 'vakyloha';
      break;
    case 'c6-c5':
      if (board[23] === 'zero eaten'){
        game_type = 'kobana';
      } else if (board[26] === 'zero eaten'){
        game_type = 'fohy';
      }
      break;
    case 'd4-c5':
      game_type = 'havanana';
      break;
    case 'd6-c5':
      game_type = 'havia';
      break;

      default:
        break;
  }
  return game_type;
}


export function make_computer_move(board, moves){
  let boardstate = board;
  const selected = moves[0];
  const eaten = moves[1];
  boardstate = new_board(boardstate);
  if (eaten.length === 0){
    // boardstate[selected] = 'zero visited';
    // return boardstate;
    alert('Bad eaten/moves');
    return boardstate;
  }
  for (var j=0; j<eaten.length; j++){
    if (boardstate[eaten[j]] === 'one') {
      boardstate[eaten[j]] = 'zero eaten';
    } else{
      boardstate[eaten[j]] = 'zero';
    }
  }
  boardstate[selected] = 'two selected visited';
  return boardstate;
}


export function un_mark(board, list_keys){
  let boardout = board.slice();
  for (var i = 0; i<50; i++) {
    for (var j = 0; j < list_keys.length; j++) {
      boardout[i] = boardout[i].replace(' ' + list_keys[j], '');
    }
  }
  return boardout;
}


export function undo_selected(board){
    return un_mark(board, ['available', 'selected']);
}


export function new_board(board){
  let keys = ['selected', 'choose', 'available', 'visited', 'eaten', 'animated', 'newpos'];
  return un_mark(board, keys);
}

export function un_mark_available(board){
  return un_mark(board, ['available', 'selected']);
}


export function has_keys(board, keys){
  for (var i = 0; i<50; i++){
    let piece = board[i];
    if (piece.includes(keys)){
      return i;
    }
  }
  return -1
}


export function has_selected(board){
  return has_keys(board, 'selected')
}


export function get_newpos(board){
  return has_keys(board, 'newpos')
}



export function get_pieces(board, keys){
  let outlist=[];
  for (var i = 0; i<50; i++){
    const piece = board[i];
    if (piece.includes(keys)){
      outlist.push(i);
    }
  }
  return outlist;
}


export function has_available(board){
  return get_pieces(board, 'available');
}


export function get_eaten(board){
  return get_pieces(board, 'eaten');
}


export function visited(board){
  return get_pieces(board, 'visited');
}


export function must_choose(board){
  return get_pieces(board, 'choose');
}


export function mark_piece(board, piece, keys){
  board[piece] = board[piece] + ' '+keys;
  return board;
}

export function mark_available(board, piece){
  return mark_piece(board, piece, 'available');
}

export function mark_selected(board, piece){
  return mark_piece(board, piece, 'selected');
}

export function mark_possible_move(boardstat, piece, visited, has_moved) {
  let boardstate = boardstat.slice();
  boardstate = un_mark_available(boardstate);
  // visited.push(piece);
  let pos;
  let must_capture = MustCapture(boardstate, has_moved);
  let possible_move = legalMove(boardstate, piece, visited, must_capture);
  mark_selected(boardstate, piece);
  if (possible_move.length > 0) {
    for (var j = 0; j < possible_move.length; j++) {
      pos = possible_move[j];
      mark_available(boardstate, pos);
    }
    return [true, boardstate];
  } else{
    return [false, boardstate];
  }

}



export function ToSquare(id) {
    var column = 10 - (id % 10);
    var row = ~~(id / 10);
    var lookup = { "0":"e", "1":"d", "2":"c","3":"b", "4":"a"};
    return lookup[row]+column;
}


export function count_pieces(board) {
  let my_pieces_count = 0;
  let opp_pieces_count = 0;
  for (var i = 0; i<50; i++){
    const piece = board[i].split(' ')[0];
    if (piece === 'one'){
      ++my_pieces_count;
    } else if (piece === 'two') {
      ++opp_pieces_count;
    }
  }
  return [my_pieces_count, opp_pieces_count]
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
      new_history.push({turn:i/2+1, human:history_turn[i].visited, computer:" "});
    } else{
      item = new_history[new_history.length -1]
      item.computer= history_turn[i].visited;
    }
  }
  return new_history;
}


export function piece_can_capture(boardstate, id) {
  var valid_move, capture;
  // var last_move, last_id;
  if ((id % 2) !== ( (~~ (id / 10)
  ) % 2)) {
  valid_move = [-11, -10, -9, -1, 1, 9, 10, 11];
  } else{
  valid_move = [-10, -1, 1, 10];
  }
  for (var i=0; i<valid_move.length; i++){
    var next_move = id + valid_move[i];
    if (((next_move % 10) === 0) || (next_move < 0) || (next_move > 49)) {
        continue;
    }
    let piece = boardstate[next_move];
    capture = can_capture(boardstate, id, valid_move[i])
    if ((piece.includes('zero')) && capture){
        return true
    }
  }
  return false;
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
    if (((next_move % 10) === 0) || (next_move < 0) || (next_move > 49)) {
        continue;
    }
    let piece = boardstate[next_move];
    // console.log(piece, next_move);
    if (((piece === 'zero') || (piece.includes('zero eaten')))  && !
  (visited.includes(next_move))){
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


export function board_has_capture(boardstate){
    const my_pieces_idx = boardstate.reduce((a, e, i) => (e === 'one') ? a.concat(i) : a, []);
    // var visited = [];
    for (var i=0; i<my_pieces_idx.length; i++){
      if (piece_can_capture(boardstate, my_pieces_idx[i])){
            return true;
      }
    }
    return false;
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


export function makeMove_choosen(boardstate, visits, selected, newpos, choosen){
  var movetype = newpos - selected;
  var direction, pos_eat;
  boardstate = un_mark(boardstate, ['eaten', 'choose', 'available', 'selected']);

  if ((selected + 2*movetype) === choosen){
    direction = movetype;
    pos_eat = newpos + direction;
  } else if ((selected - movetype) === choosen){
    direction = -movetype;
    pos_eat = newpos + 2*direction;
  }
  boardstate[selected] = 'zero visited';
  boardstate[newpos] = 'one';
  while (boardstate[pos_eat] === 'two'){
      boardstate[pos_eat] = 'zero eaten';
      pos_eat = pos_eat + direction;
  }
  visits.push(newpos);
  return mark_possible_move(boardstate, newpos, visits, true);
}


export function makeMove(boardstate, visits, selected, newpos, movetype){
    var direction;
    var pos_eat;
    let was_pass = false;
    boardstate = un_mark(boardstate, ['eaten', 'animated', 'available', 'selected']);

    if (boardstate[selected + 2*movetype] === 'two'){
        direction = movetype;
        pos_eat = newpos + direction;
    } else if (boardstate[selected - movetype] === 'two'){
        direction = -movetype;
        pos_eat = newpos + 2*direction;
    } else{
      was_pass = true
    }

    // If our move did not capture opponent piece => not allow to move again
    if (!(was_pass)) {
      boardstate[selected] = 'zero visited';
      boardstate[newpos] = 'one';
      while (boardstate[pos_eat] === 'two'){
        boardstate[pos_eat] = 'zero eaten';
        pos_eat = pos_eat + direction;
      }
      // const visits = visited(boardstate);
      visits.push(newpos);
      return mark_possible_move(boardstate, newpos, visits, true);
    } else{
      boardstate[selected] = 'zero';
      boardstate[newpos] = 'one';
      return [false, boardstate];
    }

  }
  

export function MustCapture(boardstate, has_moved){
  if (has_moved){
    return true;
  } else {
    return board_has_capture(boardstate);
  }
}

export function is_winner(board){
  let [my_pieces_count, opp_pieces_count] = count_pieces(board)
  if (my_pieces_count === 0){
    return 'Computer WIN';
  } else if (opp_pieces_count === 0){
    return 'You WIN';
  } else {
    return null;
  }
}

export function  has_winner(newboard){
  const winner = is_winner(newboard);
  if (winner){
    alert("game over: " + winner);
    return true;
  } else {
    return false;
  }
}



export  function get_board(gametype){
  let board;
  if (gametype === 'vakyloha'){
    board = ["zero","one","one","one","one","zero eaten","one","one","one","one",
      "zero","one","one","one","one","zero eaten","one","one","one","one",
      "zero","two","one","two","one","two","two","one","two","one",
      "zero","two","two","two","two","zero","two","two","two","two",
      "zero","two","two","two","two","two","two","two","two","two"];
  } else if (gametype === 'kobana') {
    board = [ "zero","one","one","one","one","one","one","one","one","one",
    "zero","one","one","one","one","one","one","one","one","one",
    "zero","two","one","two","one","two","zero","zero eaten","two","one",
    "zero","two","two","two","two","two","two","two","two","two",
    "zero","two","two","two","two","two","two","two","two","two"
  ];
  } else if (gametype === 'fohy') {
    board = ["zero","one","one","one","one","one","one","one","one","one",
    "zero","one","one","one","one","one","one","one","one","one",
    "zero","two","one","two","zero eaten","two","zero","one","two","one",
    "zero","two","two","two","two","two","two","two","two","two",
    "zero","two","two","two","two","two","two","two","two","two"
              ];
  } else if (gametype === 'havia') {
    board = [ "zero","one","one","zero eaten","one","one","one","one","one","one",
              "zero","one","one","one","zero eaten","one","one","one","one","one",
              "zero","two","one","two","one","two","two","one","two","one",
              "zero","two","two","two","two","two","zero","two","two","two",
              "zero","two","two","two","two","two","two","two","two","two"
              ];
  } else if (gametype === 'havanana'){
    board = [ "zero","one","one","one","one","one","one","zero eaten","one","one",
              "zero","one","one","one","one","one","zero eaten","one","one","one",
              "zero","two","one","two","one","two","two","one","two","one",
              "zero","two","two","two","zero","two","two","two","two","two",
              "zero","two","two","two","two","two","two","two","two","two"
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
