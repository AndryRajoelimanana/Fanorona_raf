export function create_board(my_pieces, opp_pieces){
    var stones = Array(50).fill('zero');
    var my_pieces_binrepr = (my_pieces).toString(2).padStart(64,'0');
    var opp_pieces_binrepr = (opp_pieces).toString(2).padStart(64,'0');
    var my_len = my_pieces_binrepr.length;
    var opp_len = opp_pieces_binrepr.length;  
    for (var i = 0; i < 50; i++) {
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


export function has_available(board){
  let available_move=[];
  for (var i = 0; i<50; i++){
    const piece = board[i];
    if (piece.includes('available')){
      available_move.push(i);
    }
  }
  return available_move;
}


export function get_eaten(board){
  let eaten=[];
  for (var i = 0; i<50; i++){
    const piece = board[i];
    if (piece.includes('eaten')){
      eaten.push(i);
    }
  }
  return eaten;
}


export function visited(board){
  let visits=[];
  for (var i = 0; i<50; i++){
    const piece = board[i];
    if (piece.includes('visited')){
      visits.push(i);
    }
  }
  return visits;
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

export function must_choose(board){
  let choose=[];
  for (var i = 0; i<50; i++){
    const piece = board[i];
    if (piece.includes('choose')){
      choose.push(i);
    }
  }
  return choose;
}

export function make_computer_move(board, moves){
  let boardstate = board;
  const selected = moves[0];
  const eaten = moves[1];
  boardstate = new_board(boardstate);
  if (eaten.length === 0){
    boardstate[selected] = 'zero visited';
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


export function undo_selected(board){
  let boardout = board.slice();
  for (var i = 0; i<50; i++){
    const piece = boardout[i];
    boardout[i] = piece.replace(' selected','');
    boardout[i] = piece.replace(' available','');
    // if (piece.includes('selected')){
    //  board[i] = piece.replace(' selected','');
    }
  return board;
}

export function new_board(board){
  let boardout = board.slice();
  for (var i = 0; i<50; i++){
    boardout[i] = boardout[i].replace(' selected','');
    boardout[i] = boardout[i].replace(' available','');
    boardout[i] = boardout[i].replace(' choose','');
    boardout[i] = boardout[i].replace(' visited','');
    boardout[i] = boardout[i].replace(' eaten','');
    boardout[i] = boardout[i].replace(' animated','');
    boardout[i] = boardout[i].replace(' newpos','');
    }
  return boardout;
}

export function un_mark_available(board){
  let boardout = board.slice();
  for (var i = 0; i<50; i++){
    boardout[i] = boardout[i].replace(' available','');
    boardout[i] = boardout[i].replace(' selected','');
    }
  return boardout;
}


export function mark_possible_move(boardstat, piece, visited, has_moved) {
  let boardstate = boardstat.slice();
  boardstate = un_mark_available(boardstate);
  visited.push(piece);
  let pos;
  let must_capture = MustCapture(boardstate, has_moved);
  let possible_move = legalMove(boardstate, piece, visited, must_capture);
  boardstate[piece] = boardstate[piece] + ' selected';
  if (possible_move.length > 0) {
    for (var j = 0; j < possible_move.length; j++) {
      pos = possible_move[j];
      boardstate[pos] = boardstate[pos] + ' available';
    }
    return [true, boardstate];
  } else{
    return [false, new_board(boardstate)];
  }

}


export function has_selected(board){
  for (var i = 0; i<50; i++){
    let piece = board[i];
    if (piece.includes('selected')){
      return i;
    }
  }
  return -1
}


export function get_newpos(board){
  for (var i = 0; i<50; i++){
    let piece = board[i];
    if (piece.includes('newpos')){
      return i;
    }
  }
  return -1
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
      new_history.push({turn:i/2+1, human:history_turn[i].human, computer:" "});
    } else{
      item = new_history[new_history.length -1]
      item.computer= history_turn[i].human;
    }
  }
  return new_history;
}


export function getTurn1(history_turn){
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
    if (((next_move % 10) === 0) || (next_move < 0)) {
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


export function makeMove_choosen(boardstate, selected, newpos, choosen){
  var movetype = newpos - selected;
  var direction, pos_eat;
  for (var i = 0; i<50; i++){
      boardstate[i] = boardstate[i].replace(' eaten','');
      boardstate[i] = boardstate[i].replace(' available','');
      boardstate[i] = boardstate[i].replace(' selected','');
      boardstate[i] = boardstate[i].replace(' choose','');
    }
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
  const visits = visited(boardstate);
  visits.push(selected);
  return mark_possible_move(boardstate, newpos, visits, true);
}


export function makeMove(boardstate, selected, newpos, movetype){
    var direction;
    var pos_eat;
    let was_pass = false;
    for (var i = 0; i<50; i++){
      boardstate[i] = boardstate[i].replace(' eaten','');
      boardstate[i] = boardstate[i].replace(' available','');
      boardstate[i] = boardstate[i].replace(' selected','');
      boardstate[i] = boardstate[i].replace(' animated','');
    }
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
      const visits = visited(boardstate);
      visits.push(selected);
      return mark_possible_move(boardstate, newpos, visits, true);
    } else{
      boardstate[selected] = 'zero';
      boardstate[newpos] = 'one';
      return [false, boardstate];
    }

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
