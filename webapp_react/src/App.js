import React from 'react';
// import {PathLine} from 'react-svg-pathline'
import './App.css';
import * as utils from './utils.js';
import axios from 'axios';


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      width: 100,
      height: 100,
      history: [{
        boardState: utils.create_board(17353881, 562399469895680),
        currentPlayer: true,
      }],
      my_pieces: 173538815,
      opp_pieces: 56695680,
      selected: null,
      step_number: 0,
      has_moved: null,
      available_move: [],
      visited:[],
      must_choose:[],
    };
  }


  getCurrentState() {
    var history = this.state.history;
    if (history.length > 1){
      history = history.slice(0, this.state.step_number + 1);
      return history[history.length - 1];
    } else {
      return history[0];
    }
  }

  resetState(newboard) {
    this.setState({history: this.state.history.concat([{
      boardState: newboard, 
      currentPlayer: true,}]),
    selected: null, 
    available_move: [],
    has_moved: false,
    visited: [],
    must_choose: false,
    step_number: this.state.history.length,
  });
  }

  get_AI_move(boardstate, was_capture) {
    let current_params = {'boardstate':boardstate, 'was_capture':was_capture};
    axios.post('/pass', current_params)
    .then(res => {
        return res;
    })
    .catch(err => {
        console.log(err);
        alert(err);});
  }
  


  onClick = (i) => {
    const selected = this.state.selected;
    const currentState = this.getCurrentState();
    const boardstate = currentState.boardState;
    const available_move = this.state.available_move;
    const visited = this.state.visited;
    const must_choose = this.state.must_choose;
    var movetype;
    var possible_move;
    var must_capture;
    var result;
    var was_capture = true;
    // if clicked the selected piece twice undo selection
    if ((selected === i) && (!this.state.has_moved)) {
      this.setState({selected: null, available_move: []});
      return;
    }

    /* if no piece was selected:
      - return if the next selected is not my_pieces
      - else: check if the selected piece can move and return available move
    */
    if (this.state.has_moved){
        must_capture = true;
    } else{
        must_capture = utils.has_capture(boardstate);
    }
    
    if (!(selected)){
      if (boardstate[i] !== 'one'){
        return
      }
      possible_move = utils.legalMove(boardstate, i, visited, must_capture);
      // if it can move mark it as selected and show available move
      if (possible_move.length > 0){
        this.setState({selected: i, available_move: possible_move});
      }
    }

    if (must_choose.length>1){
      if (!(must_choose.includes(i))){
        alert("you must choose");
        return
      } else{
        movetype = i - selected;
      }
    }

    if (available_move.includes(i)){
      movetype = i - selected;
      const capture_forward = selected + 2*movetype;
      const capture_backward = selected - movetype;
      if ((boardstate[capture_forward] ==='two') && (boardstate[capture_backward] ==='two')){
        alert('must choose');
        this.setState({must_choose: true});
      }
      var newboard = utils.makeMove(boardstate, selected, i, movetype);
      if (!must_capture){
        this.resetState(newboard);
        result = this.get_AI_move(boardstate, was_capture);
        this.resetState(result.boardstate);
      }
      visited.push(selected);
      visited.push(i);
      possible_move = utils.legalMove(newboard, i, visited, must_capture);
      console.log(newboard);
      if ((possible_move.length>=1) && (must_capture)){
        this.setState({history: this.state.history.concat([{
          boardState: newboard, 
          currentPlayer: true,}]),
        selected: i, 
        available_move: possible_move,
        has_moved: true,
        visited: visited,
        must_choose: false,
        step_number: this.state.history.length,});
      } else{
          this.resetState(newboard);
          result = this.get_AI_move(boardstate, was_capture);
          this.resetState(result.boardstate);
          return;
      }
    }
  }

  

  render() {
    const state_history = this.state.history;
    const current_state = state_history[this.state.step_number];
    const boardstate = current_state.boardState;
    const selected = this.state.selected;
    const available_move = this.state.available_move;
    return (
      <div className='main'>
        <div className='game_windows align="center"'>
          <div className="crosscont">
          <Board
              boardstate={boardstate}
              selected = {selected}
              available_move = {available_move}
              onClick={i => this.onClick(i)}
            />
          </div>
        </div>-
      </div>
    )
  }
};

// const computer='two';

const Stones = (props) => {
  const id = props.id;
  const idbox = utils.ToSquare(id);
  const selected = props.selected;
  const available = props.available;
  var classname = "player-"+props.stoneClasses +' '+idbox;
  if (id === selected){
    classname = classname + '  selected';
  }
  if (available.indexOf(id) > -1) {
    classname = classname + '  available';
  }  
  return (
      <div className={classname}  id={id} onClick={props.onClick}>
      </div>
  );
}


class Board extends React.Component {
  RenderStones = (i) => {
    const stone = this.props.boardstate[i];
    const selected = this.props.selected;
    const available = this.props.available_move;
    return (
      <Stones stoneClasses={stone} id={i} selected={selected}  available={available} onClick={() => this.props.onClick(i)}
      />
  );
  }
  render() {
    return (
      <div className="rowcross">
        <div className='crossed'>
          {this.RenderStones(49)}
          {this.RenderStones(48)}
          {this.RenderStones(39)}
          {this.RenderStones(38)}
          </div>
        <div className='crossed'>
          {this.RenderStones(47)}
          {this.RenderStones(46)}
          {this.RenderStones(37)}
          {this.RenderStones(36)}
          </div>
        <div className='crossed'>
          {this.RenderStones(45)}
          {this.RenderStones(44)}
          {this.RenderStones(35)}
          {this.RenderStones(34)}
          </div>
        <div className='crossed_left'>
          {this.RenderStones(43)}
          {this.RenderStones(42)}
          {this.RenderStones(41)}
          {this.RenderStones(33)}
          {this.RenderStones(32)}
          {this.RenderStones(31)}
          </div>
        <div className='crossed_bottom'>
          {this.RenderStones(29)}
          {this.RenderStones(28)}
          {this.RenderStones(19)}
          {this.RenderStones(18)}
          {this.RenderStones(9)}
          {this.RenderStones(8)}
          </div>
        <div className='crossed_bottom'> 
          {this.RenderStones(27)}
          {this.RenderStones(26)}
          {this.RenderStones(17)}
          {this.RenderStones(16)} 
          {this.RenderStones(7)}
          {this.RenderStones(6)}                  
          </div>
        <div className='crossed_bottom'>
          {this.RenderStones(25)}
          {this.RenderStones(24)}
          {this.RenderStones(15)}
          {this.RenderStones(14)}
          {this.RenderStones(5)}
          {this.RenderStones(4)}          
          </div>
        <div className='crossed_bottom_left'>
          {this.RenderStones(23)}
          {this.RenderStones(22)}
          {this.RenderStones(21)}
          {this.RenderStones(13)}
          {this.RenderStones(12)}
          {this.RenderStones(11)}
          {this.RenderStones(3)}
          {this.RenderStones(2)}
          {this.RenderStones(1)}
          </div>
      </div>
    );
  }
}


export default App;
