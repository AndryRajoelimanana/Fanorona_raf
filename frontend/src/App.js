import React from 'react';
// import {PathLine} from 'react-svg-pathline'
import './App.css';
import * as utils from './utils.js';
import axios from 'axios';
import { Container, Row, Col, Form} from 'react-bootstrap';
import BoardRender from "./components/board/board.js";
import MoveStatus from "./components/Move/MoveStatus.js";
import { MoveFirst, GameType, SearchDepth } from "./components/Menu/game_options.js";
import GameOptionsBar from "./components/Menu/command_button.js";


class App extends React.Component {
  constructor(props) {
    super(props);
    this.initialState = {
      depth: 3,
      turn_id: 1,
      boardstate: utils.create_board(346553855, 562399296880640),
      status: '',
      visited: [],
      game_type:'',
      move_first:'human',
      wait_ai: false,
      history_turn: [{
        boardState: [{boardState: utils.create_board(346553855, 562399296880640)}],
        turn_id: 1, visited:[]
      }],
    }
    this.state = this.initialState;
    this.undo_move = this.undo_move.bind(this);
    this.pass_game = this.pass_game.bind(this);
    this.restart_board = this.restart_board.bind(this);
  }

  restart_board = () => {
    this.setState(() => {return this.initialState});
  }

  async wait_here(time_wait) {
    await delay(time_wait);
  }

  async update_board(board, move) {
    let newboard = await utils.make_computer_move(board, move);
    this.setState(() => ({boardstate: newboard}));
    return newboard;
  }


  componentDidUpdate = (prevProps, prevState) => {
    if (this.state.turn_id !== prevState.turn_id){
      let bb = utils.new_board(this.fetch_board());
      if ((this.state.turn_id % 2) === 0){
        this.setState(() => ({wait_ai: true}));
        var board = bb.slice();
        const depth = this.state.depth;
        let current_params = {'boardstate':board, 'depth':depth};
        var selected_list = [];
        axios.post('/pass', current_params).then(async (res) => {
          let move_log = res.data["move_log"];
          var newboard = bb.slice();
          for (var i=0; i<move_log.length; i++){
            selected_list.push(move_log[i][0]);
            newboard = await this.update_board(newboard, move_log[i]);
            await this.wait_here(600)
          }
          const turn = this.increase_turn();
          const move_string = utils.tomoveString(selected_list);
          const history = {boardState: utils.new_board(newboard), turn_id:
  turn, visited:move_string};
          const history_turn = this.AppendHistory(history);

          this.setState(() => ({boardstate: utils.new_board(newboard),
  turn_id:turn, history_turn:history_turn}));
        if (this.check_winner(newboard)){
          this.restart_board();
          return;
        }
        }
        ).catch(err => {
          alert(err);
        });
        this.setState(() => ({wait_ai: false}));
      }
    }
  }


  AppendHistory(history) {
    var history_turn = this.state.history_turn.slice();
    return history_turn.concat([history])
  }


  undo_move = () => {
    const turn = this.fetch_turn_id()
    if (turn % 2 === 0){
      return;
    }
    let currTurn = this.fetch_turn_id();
    currTurn = currTurn - 2;
    if (currTurn <= 1){
      this.restart_board();
      return
    }
    let prev_hist_turn = this.state.history_turn.slice(0, currTurn);
    let board = prev_hist_turn[currTurn-1].boardState;
    this.setState(() => ({history_turn:prev_hist_turn, boardstate:board,
  turn_id:currTurn, visited:[], }));
  }

  check_winner(newboard){
    if (utils.has_winner(newboard)){
      this.restart_board();
    }
  }

  pass_game = async () => {
    const turn = this.fetch_turn_id()
    if (turn % 2 === 0){
      return;
    }
    let visited = this.fetch_visited();
    if (visited.length === 0){
      return;
    }
    const newboard = this.fetch_board();
    await this.reset_newboard(newboard, this.fetch_visited());
  }

  handle_game_type = (event) =>{
    const game_type = event.target.value;
    let board = utils.get_board(game_type);
    this.restart_board();
    this.setState({boardstate: board,
      history_turn: [{boardState: board,turn_id: 1}],
      game_type: game_type,
      status: 'human to move',
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

  reset_newboard = async (board, visited) =>{
    console.log(this.state.turn_id, visited);
    this.setState(() => ({boardstate: board, visited:visited}));
    await this.wait_here(300);
    let newboard = utils.new_board(board);
    const turn = this.increase_turn();
    const move_string = utils.tomoveString(visited);
    if (turn === 2){  // turn is already updated to turn + 1
      let game_type = utils.get_first_move(newboard, move_string)
      console.log('gametype '+game_type);
      this.setState(() => ({game_type: game_type}));
    }
    const history = {boardState: newboard, turn_id: turn, visited:move_string};
    const history_turn = this.AppendHistory(history);
    await this.wait_here(300);
    this.setState(() => ({boardstate: newboard, turn_id:turn,visited:[], history_turn:history_turn}));
    if (this.check_winner(newboard)){
      this.restart_board();
      return;
    }
  }

  fetch_board = () => {return this.state.boardstate};
  fetch_turn_id = () => {return this.state.turn_id};
  fetch_visited = () => {return this.state.visited};
  wait_computer = () => {return this.state.wait_ai};

  onClick = async (i) => {
    const turn_id = this.state.turn_id;
    console.log(turn_id);
    if (turn_id % 2 === 0){
      return
    }
    const boardstate = this.fetch_board();
    let visited = this.fetch_visited();
    console.log(boardstate);
    // First moved pieces not selected
    const selected = utils.has_selected(boardstate);
    const has_moved = visited.length > 1;
    let board, will_move;

    if (! (has_moved)){
      if (selected === -1){
        if (boardstate[i] !== 'one'){
          return;
        } else {
            [will_move, board] = utils.mark_possible_move(boardstate, i, [],false);
            this.setState(() => ({boardstate: board, visited:[i]}));
            return;
        }
      } else if (selected === i) {    // if the selected piece was clicked twice undo selection
        board = utils.new_board(boardstate)
        this.setState(() => ({boardstate: board, visited:[]}));
        return;
      } else {  // clicked another piece of one
        if (boardstate[i] === 'one'){
          board = utils.new_board(boardstate);
          let board1;
          [will_move, board1] = utils.mark_possible_move(board, i, [], false);
          if (will_move){
            this.setState(() => ({boardstate: board1, visited:[i]} ));
            return;
          } else {
            return;
          }
        }
      }
    }

    // previous selection must choose direction
    const available_move = utils.has_available(boardstate)
    const must_choose = utils.must_choose(boardstate);

    let movetype;
    let capture_backward, capture_forward;


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
          alert('We cannot find new pos');
          return
        }
        let newboard
        [will_move, newboard] = utils.makeMove_choosen(boardstate,visited, selected,new_pos, i);
        if (this.check_winner(newboard)){
          this.restart_board();
          return
        }
        if (will_move){
          this.setState(() => ({boardstate: newboard, visited:visited}));
          await this.wait_here(300);
          return;
        } else {
          await this.reset_newboard(newboard, visited);
          return;
        }
      }
    }

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
        return
      }
      let newboard1;
      [will_move, newboard1] = utils.makeMove(boardstate, visited, selected, i, movetype);
      if (this.check_winner(newboard1)){
        this.restart_board();
        return
      }

      if (will_move){
        this.setState(() => ({boardstate: newboard1, visited:visited}));
        await this.wait_here(300);
      } else {
        console.log('tato', newboard1);
        await this.reset_newboard(newboard1, visited);
      }
      return
    }
  }

  render() {

    const turn_id = this.state.turn_id;
    const boardstate = this.state.boardstate;
    const selected = utils.has_selected(boardstate);
    const available_move = utils.has_available(boardstate);
    const must_choose = utils.must_choose(boardstate);
    const eaten = utils.get_eaten(boardstate);
    console.log(turn_id);
    console.log(boardstate);
    let status;
    if (turn_id % 2 === 0){
      status = 'AI is searching...';
    } else if (must_choose.length){
      status = 'Choose: '+utils.ToSquare(must_choose[0])+' or '+utils.ToSquare(must_choose[1]);
      alert("Choose between "+utils.ToSquare(must_choose[0])+' and '+utils.ToSquare(must_choose[1]));
    } else if (selected !== -1){
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
          <Row>
            <Col xs={12} sm={12} md={8}>
              <Form className='form_command'>
                  <Form.Row className="justify-content-md-center">
                    <MoveFirst move_first={this.state.move_first} onChange={this.handle_move_first}/>
                    <GameType disabled_game={disabled_game} game_type={this.state.game_type} onChange={this.handle_game_type} />
                    <SearchDepth depth={this.state.depth} onChange={this.handle_depth}/>
                  </Form.Row>
              </Form>
            </Col>
          </Row>

          <Row>
              <Row noGutters={true}> 
                <Col xs={12} sm={12} md={8}  className='game_windows row-eq-height'>
                  <div className='aspect_ratiodiv'>
                    <Container fluid={true} className='BoardCont' >
                        <Row noGutters={true} className="crosscont"  >
                          <div className='aspect_ratiodiv1'>
                          <BoardRender
                            boardstate={boardstate}
                            selected = {selected}
                            available_move = {available_move}
                            choose = {must_choose}
                            eaten = {eaten}
                            turn_id = {turn_id}
                            onClick={i => this.onClick(i)}
                          />
                          </div>
                        </Row>
                        <Row noGutters={true} className="command_button" >
                          <GameOptionsBar createNewGame={this.restart_board} passgame={this.pass_game} undogame={this.undo_move} />
                        </Row>
                        
                    </Container>
                  </div>
                </Col>
                <Col xs={12} sm={12} md={4} className="status_window row-eq-height">
                    <MoveStatus status={status} move_string={new_history} />
                </Col>
              </Row>
          </Row>
        </Container>
      </div>
    )
  }
};

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

export default App;

