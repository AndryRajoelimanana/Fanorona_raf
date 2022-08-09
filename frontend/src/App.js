import React from 'react';
// import {PathLine} from 'react-svg-pathline'
import './App.css';
import * as utils from './utils.js';
import axios from 'axios';
import { Container, Row, Col, Form} from 'react-bootstrap';
import Board from "./components/board/board.js";
import MoveStatus from "./components/Move/MoveStatus.js";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.initialState = {
      history: [{boardState: utils.create_board(346553855, 562399296880640)}],
      depth: 3,
      turn_id: 1,
      boardstate: utils.create_board(346553855, 562399296880640),
      selected: null,
      step_number: 0,
      has_moved: null,
      visited: [],
      must_choose: [],
      computer_move: false,
      is_moving: false,
      was_capture: false,
      status: null,
      game_type:null,
      move_log:[],
      move_first:'human',
      history_turn: [{
        boardState: [],
        turn_id: 0,
        human:'',
        computer:'',
      }],
      turn_number: 1,
    }
    this.state = this.initialState;

  }

  restart_board = () => {
    this.setState(this.initialState);
    // this.setState({visited:[], computer_move: false});
  }

  // const sleep = milliseconds => Atomics.wait(new Int32Array(new
  // SharedArrayBuffer(4)), 0, 0, milliseconds)
  syncWait = ms => {
      const end = Date.now() + ms
      while (Date.now() < end) continue
  }



  componentDidUpdate = (prevProps, prevState) => {
    if (this.state.turn_id !== prevState.turn_id){
      let bb = utils.new_board(this.fetch_board());
      // this.setState(() => ({boardstate: bb}));
      if ((this.state.turn_id % 2) === 0){
        let newboard = bb.slice();
        const depth = this.state.depth;
        let current_params = {'boardstate':newboard, 'depth':depth};
        let move_log;
        var selected_list = [];
        axios.post('/pass', current_params).then(res => {
          move_log = res.data["move_log"];
          for (var i=0; i<move_log.length; i++){
            selected_list.push(move_log[i][0]);
            newboard = utils.make_computer_move(newboard, move_log[i]);
            //setTimeout(()=> {

            this.setState(() => ({boardstate: newboard}));
            // this.syncWait(1000);
            // setTimeout(() => {  console.log("World!"); }, 1000);
            //}, 1);
          }
          const turn = this.increase_turn();
          const move_string = utils.tomoveString(selected_list);
          const history = {boardState: utils.new_board(newboard), turn_id:
  turn};
          const history_turn = this.AppendHistory(history);
          this.setState(() => ({boardstate: utils.new_board(newboard),
  turn_id:turn,history_turn:history_turn}));
          console.log(this.fetch_board());
        }).catch(err => {
          alert(err);
        });
      }
    }
  }


  AppendHistory(history) {
    var history_turn = this.state.history_turn.slice();
    return history_turn.concat([history])
  }


  undo_move = () => {
    let currTurn = this.fetch_turn_id();
    currTurn = currTurn - 2;
    if (currTurn <= 0){
      this.restart_board();
      return
    }
    let prev_turn;
    let board;
    let unsetHistory, prev_hist_turn;
    prev_turn = this.state.history_turn[currTurn].turn_id;
    prev_hist_turn = this.state.history_turn.slice(0, currTurn);
    board = prev_hist_turn[prev_hist_turn.length-1].boardState;
    console.log(prev_hist_turn);
    this.setState(() => ({history_turn:prev_hist_turn, boardstate:board,
  turn_id:prev_turn}));
  }

  check_winner(newboard){
    const winner = utils.is_winner(newboard);
    if (winner){
      alert("game over: " + winner);
      this.restart_board();
      return true;
    } else {
      return false;
    }

  }


  pass_game = () => {
    const newboard = this.fetch_board();
    this.reset_newboard(newboard);
  }

  handle_game_type = (event) =>{
    const game_type = event.target.value;
    this.restart_board();
    this.setState({history: [{
      boardState: utils.get_board(game_type), 
      }],
      history_turn: [{
        boardState: utils.get_board(game_type),
        turn_id: 0,
        human:'',
        computer:'',
        }],
      game_type: game_type,
      status: 'human to move',
      visited:[],
      move_first: 'computer',
    });
  }

  handle_move_first = (event) =>{
    this.restart_board();
    this.setState({move_first: event.target.value});
  }


  handle_depth = (event) =>{
    this.setState({depth: event.target.value});
  }

  increase_turn = () => {return this.state.turn_id+1;}


  reset_newboard = (board) =>{
    let newboard;
    newboard = utils.new_board(board);
    const turn = this.increase_turn();
    const visited = utils.visited(newboard);
    const move_string = utils.tomoveString(visited);
    if (turn === 1){
      let game_type = utils.get_first_move(newboard, move_string)
      console.log('gametype'+game_type);
      this.setState(() => ({game_type: game_type}));
    }
    const history = {boardState: newboard, turn_id: turn};
    const history_turn = this.AppendHistory(history);

    this.setState(() => ({boardstate: newboard, turn_id:
  turn, history_turn:history_turn}));
  }

  fetch_board = () => {return this.state.boardstate};
  fetch_turn_id = () => {return this.state.turn_id};

  onClick = (i) => {
    const turn_id = this.state.turn_id;
    console.log(turn_id);
    if (turn_id % 2 === 0){
      return
    }
    const boardstate = this.fetch_board();
    console.log(boardstate);
    // First moved pieces not selected
    const selected = utils.has_selected(boardstate);
    const visited = utils.visited(boardstate);
    const has_moved = visited.length > 0;
    let board;

    if (! (has_moved)){
      if ((selected === -1) && (boardstate[i] === 'one')){
        board = utils.mark_possible_move(boardstate, i, [], false);
        this.setState(() => ({boardstate: board}));
        return;
      } else if (selected === i) {    // if the selected piece was clicked twice undo selection
        board = utils.undo_selected(boardstate)
        this.setState(() => ({boardstate: board}));
        return;
      } else {  // clicked another piece of one
        if (boardstate[i] === 'one'){
          board = utils.undo_selected(boardstate);
          board = utils.mark_possible_move(board, i, [], false);
          const new_available_move = utils.has_available(board);
          if (new_available_move.length > 0){
            this.setState(() => ({boardstate: board}));
            return;
          } else {
            this.reset_newboard(board);
            return;
          }
        } //else{
          //board = utils.makeMove(boardstate, selected, i, movetype);
          // board = utils.mark_possible_move(boardstate, i, [], false);
        //}
      }
    }

    // previous selection must choose direction
    const available_move = utils.has_available(boardstate)
    const must_choose = utils.must_choose(boardstate);

    // console.log(available_move, must_choose, selected, visited);
    let movetype, possible_move;
    // eslint-disable-next-line
    let capture_backward, capture_forward, was_capture;


    /* if no piece was selected:
      - return if the next selected is not my_pieces
      - else: check if the selected piece can move and return available move
    */

    if (must_choose.length > 1){
      if (!(must_choose.includes(i))){
        alert("You must choose between "+utils.ToSquare(must_choose[0])+' and '+utils.ToSquare(must_choose[1]));
        return
      } else {
        const new_pos = utils.get_newpos(boardstate);
        if (new_pos === -1){
          alert('We cannot vind new pos');
          return
        }
        let newboard = utils.makeMove_choosen(boardstate, selected, new_pos, i);
        if (this.check_winner(newboard)){
          this.restart_board();
          return
        }
        for (var j = 0; j < available_move.length; j++) {
          let pos = available_move[j];
          newboard[pos] = newboard[pos].replace(' available','');
        }
        newboard = utils.mark_possible_move(newboard, new_pos, visited,has_moved);
        const new_available_move = utils.has_available(newboard);
        if (new_available_move.length > 0){
          this.setState(() => ({boardstate: newboard}));
          return;
        } else {
          this.reset_newboard(newboard);
          return;
        }
      }
    }

    let must_capture = utils.MustCapture(boardstate, has_moved);

    if (!(available_move.includes(i))){
      return;
    } else{
      movetype = i - selected;
      // Check if both forward and backward direction are possible
      capture_forward = selected + 2*movetype;
      capture_backward = selected - movetype;

      if ((boardstate[capture_forward] ==='two') && (boardstate[capture_backward] ==='two')){
        boardstate[capture_forward] = boardstate[capture_forward] + ' choose';
        boardstate[capture_backward] = boardstate[capture_backward] + ' choose';
        boardstate[i] = boardstate[i] + ' newpos';
        this.setState(() => ({boardstate: boardstate}));
        alert("Choose between "+utils.ToSquare(capture_forward)+' and '+utils.ToSquare(capture_backward));
        return
      }

      let newboard1 = utils.makeMove(boardstate, selected, i, movetype);
      if (this.check_winner(newboard1)){
        this.restart_board();
        return
      }
      const new_available_move = utils.has_available(newboard1);
      if (new_available_move.length > 0){
        this.setState(() => ({boardstate: newboard1}));
        return;
      } else {
        this.reset_newboard(newboard1);
        return;
      }
      must_capture = utils.MustCapture(newboard1, true);
      if (!must_capture){
        this.reset_newboard(newboard1);
        return;
      }
      // this.setState(() => ({boardstate: newboard1}));

      // possible_move = utils.legalMove(newboard1, i, visited, must_capture);
      // if (possible_move.length>=1){
      //   this.setState({history: this.state.history.concat([{
      //     boardState: newboard1,
      //     currentPlayer: true,}]),
      //   selected: i,
      //   available_move: possible_move,
      //   has_moved: true,
      //   visited: visited,
      //   must_choose: [],
      //   step_number: this.state.history.length,});
      // } else{
      //     this.reset_newboard(newboard1);
      //     return;
      // }
    }
  }
  

  render() {
    
    // const status = this.status;

    // const boardstate = this.getCurrentState();
    const boardstate = this.state.boardstate;
    // console.log(boardstate);
    const selected = utils.has_selected(boardstate);
    const available_move = utils.has_available(boardstate);
    // console.log(available_move);
    const must_choose = utils.must_choose(boardstate);

    let status;
    if (this.state.is_moving){
      status = 'Computer is moving...';
    } else if (must_choose.length){
      status = 'Choose: '+utils.ToSquare(must_choose[0])+' or '+utils.ToSquare(must_choose[1]);
    } else if (selected){
      status = 'Piece selected: '+utils.ToSquare(selected);
    } else {
      status = 'Human to move';
    }

    const hist_in = this.state.history_turn.slice(1);
    const new_history = utils.getTurn(hist_in);
    const disabled_game = this.state.move_first === 'human' ? true : false;


    return (
      <div className='main'>
        <Container fluid={true} id={'container1'}>
          <Row noGutters={true}>
            <Col xs={12} sm={12} md={8}>
                <Form className='form_command'>
                <Form.Row className="justify-content-md-center">
                  <Form.Group as={Col} md="3" xs="4" controlId="opponent">
                    <Form.Label>Move First</Form.Label>
                    <Form.Control value={this.state.move_first} as="select" onChange={this.handle_move_first}>
                        <option value="computer">Computer</option>
                        <option value="human">Human</option>
                    </Form.Control>
                  </Form.Group>

                  <Form.Group as={Col} md="3"  xs="4" controlId="move_first">
                    <Form.Label>Game Type</Form.Label>
                    <Form.Control disabled={disabled_game}  value={this.state.game_type} as="select" onChange={this.handle_game_type} >
                      <option value="vakyloha">Vaky loha</option>
                      <option value="kobana">Kobana</option>
                      <option value="fohy">Fohy</option>
                      <option value="havia">Havia</option>
                      <option value="havanana">Havanana</option>
                    </Form.Control>
                  </Form.Group>

                  <Form.Group as={Col} md="3"  xs="4" controlId="depth">
                    <Form.Label>Depth</Form.Label>
                    <Form.Control value={this.state.depth} as="select"  onChange={this.handle_depth}>
                      <option>1</option>
                      <option>2</option>
                      <option>3</option>
                      <option>4</option>
                      <option>5</option>
                    </Form.Control>
                  </Form.Group>
                </Form.Row>
              </Form>
            </Col>
          </Row>
          <Row noGutters={true}>
            <div className='windowa'>
            <Row noGutters={true}> 
              <Col xs={12} sm={12} md={8}  className='game_windows row-eq-height'>
                <div className='aspect_ratiodiv'>
                  <Container fluid={true} className='BoardCont' >
                      <Row noGutters={true} className="crosscont"  >
                        <div className='aspect_ratiodiv1'>
                        <Board
                          boardstate={boardstate}
                          selected = {selected}
                          available_move = {available_move}
                          onClick={i => this.onClick(i)}
                        />
                        </div>
                      </Row>
                      <Row noGutters={true} className="command_button" >
                          <Col style={{ textAlign: "center" }}>
                            <button  className="game_button"  onClick={() => this.restart_board()}>Restart</button>
                          </Col>
                          <Col style={{ textAlign: "center" }}>
                            <button  className="game_button"   onClick={() => this.pass_game()}>Pass</button>
                          </Col>
                          <Col style={{ textAlign: "center" }}>
                            <button  className="game_button"   onClick={() => this.undo_move()}>Undo</button>   
                          </Col>
                      </Row>
                      
                  </Container>
                </div>
              </Col>
              <Col xs={12} sm={12} md={4} className="status_window row-eq-height">
                <MoveStatus 
                  status={status} move_string={new_history}
                  //move_table={move_table}
                />
              </Col>
            </Row>
            </div>
          </Row>
        </Container>
      </div>
    )
  }
};



// eslint-disable-next-line
const initialState = {
  history: [{
    boardState: utils.create_board(346553855, 562399296880640),
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
  history_turn: [{
    boardState: utils.create_board(346553855, 562399296880640),
    turn_id: 0,
    human:'',
    computer:'',
  }],
  turn_number: 0,
};


export default App;
