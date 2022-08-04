import React from 'react';
// import {PathLine} from 'react-svg-pathline'
import './App.css';
import * as utils from './utils.js';
import axios from 'axios';
import { Container, Row, Col, Form} from 'react-bootstrap';


class App extends React.Component {
  constructor(props) {
    super(props);
    this.initialState = {
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
      winner: false,
      history_turn: [{
        boardState: [],
        turn_id: 0,
        human:'',
        computer:'',
      }],
      turn_number: 0,
    }
    this.state = this.initialState;
  }

  restart_board = () => {
    this.setState(this.initialState);
    this.setState({visited:[], computer_move: false});
  }

  componentDidUpdate = (prevProps, prevState) => {
   // if (prevState.turn_number !== this.state.turn_number){
      if (this.state.computer_move) {
        this.setState({is_moving: true});
        setTimeout(()=> {
        this.wait_computer();
        }, 10000);
        this.setState({computer_move: false, is_moving: false});
      }
   // }
  }


  computer_turn(boardstate, was_capture, depth) {
    let current_params = {'boardstate':boardstate, 'was_capture':was_capture, 'depth':depth};
    var selected_list = [];
    var states = [];
    axios.post('/pass', current_params)
    .then(res => {
        let move_log = res.data["move_log"];
        // console.log(move_log);
        // let movedict = move_log;
        let selected;
        let prev_selected = move_log[0][0];
        for (var i=0; i<move_log.length; i++){
          selected = move_log[i][0];
          var eaten = move_log[i][1];
          boardstate = boardstate.map(function(item) { return item === 'none eaten' ? 'none' : item; });
          for (var j=0; j<eaten.length; j++){
            boardstate[eaten[j]] = 'none eaten';
          }
          // boardstate[selected] = 'two'
          // 
          // var eaten = movedict[selected];
          // for (var j=0; j<eaten.length; j++){
          //   boardstate[eaten[j]] = 'none eaten';
          // }
          selected_list = selected_list.concat([selected]);
          console.log(selected_list);
          boardstate[prev_selected] = 'none';
          prev_selected = selected;
          boardstate[prev_selected] = 'two';
          states = states.concat([boardstate]);
        }
        this.iterate_move(selected_list, states, []);
    })
    .catch(err => {
        alert(err);
    });
  }


  iterate_move(move, states, visited){
    let selected = move.shift();
    let board = states.shift();
    visited.push(selected);
    if (move.length === 0){
      this.resetState(board, false);
      return
    }
    this.setState({history: this.state.history.concat([{
        boardState: board,}]), selected: selected, step_number: this.state.history.length, visited: visited});

    setTimeout(()=> {
      this.iterate_move(move, states, visited)
    }, 600);
  }


  wait_computer(){
    const board = this.getCurrentState();
    var was_capture = this.state.was_capture;
    var depth = this.state.depth;
    this.computer_turn(board, was_capture, depth);

  }


  getCurrentState() {
    const history = this.state.history.slice();
    if (history.length > 1){
      return history[history.length - 1].boardState;
    } else {
      return history[0].boardState;
    }
  }


  AppendHistory(history) {
    var history_turn = this.state.history_turn.slice();
    return history_turn.concat([history])
  }


  undo_move = () => {
    let currTurn = this.state.turn_number;
    if (currTurn <= 2){
      this.restart_board();
      return
    }
    let prev_step;
    let unsetHistory, prev_hist_turn;
    if (currTurn % 2 === 0){
      prev_step = this.state.history_turn[currTurn-2].step_number;
      unsetHistory = this.state.history.slice(0, prev_step+1);
      prev_hist_turn = this.state.history_turn.slice(0, currTurn-1);
      currTurn = currTurn-1;
    } else{
      prev_step = this.state.history_turn[currTurn-1].step_number;
      prev_hist_turn = this.state.history_turn.slice(0, currTurn);
      unsetHistory = this.state.history.slice(0, prev_step+1);
    }
    this.setState({
        history: unsetHistory,
        history_turn: prev_hist_turn,
        selected: null,
        available_move: [],
        visited: [],
        must_choose: [],
        new_pos: null,
        step_number: prev_step,
        turn_number: currTurn-1
    });
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



  resetState = (newboard, changemove) => {
    var was_capture;

    const visited = this.state.visited.slice();
    const move_string = utils.tomoveString(visited);
    const turn = this.state.turn_number +1;
    let game_type;
    if (turn === 1){
      // eslint-disable-next-line
      switch(move_string){
        case 'd5-c5':
          game_type = 'vakyloha';
          break;
        case 'c6-c5':
          if (newboard[23] === 'none eaten'){
            game_type = 'kobana';
          } else if (newboard[26] === 'none eaten'){
            game_type = 'fohy';
          }
          break;
        case 'd4-c5':
          game_type = 'havanana';
          break;
        case 'd6-c5':
          game_type = 'havia'; 
          break;
      }
      console.log('gametype'+game_type)
      this.setState({game_type: game_type});
      
    }

    const history_turn = this.AppendHistory({boardState: newboard, step_number: this.state.history.length, turn_id: turn, human:move_string, computer:''});
    
    if (newboard.includes('none eaten')){
      was_capture = true;
    } else {
      was_capture = false;
    }
    let computer_move;
    if (changemove){
      computer_move = this.state.computer_move ? false:true;
    } else {
      computer_move = this.state.computer_move;
    }
    
    this.setState({history: this.state.history.concat([{
        boardState: newboard, }]),
      selected: null, 
      available_move: [],
      visited: [],
      has_moved: false,
      must_choose: [],
      step_number: this.state.history.length,
      status: 'Computer is moving',
      history_turn: history_turn ,
      turn_number: turn,
      was_capture: was_capture,
      computer_move: computer_move,
    });

  }


  pass_game = () => {
    if (!(this.state.has_moved)){
      return;
    }
    const visited = this.state.visited;
    const move_string = utils.tomoveString(visited);
    const turn = this.state.turn_number + 1;
    const newboard = this.getCurrentState();
    const history_turn = this.AppendHistory({boardState: newboard, step_number: this.state.history.length, turn_id: turn, human:move_string, computer:''});

    this.setState({was_capture: true, computer_move: true, 
      selected: null, status: 'Computer is moving',
      available_move: [],
      visited: [],
      has_moved: false,
      must_choose: [],
      history_turn: history_turn,
      turn_number: turn,
    });
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


  onClick = (i) => {
    if (this.state.computer_move){
      return
    }
    if (this.state.move_first === 'computer'){
      if (!(this.state.status)){
        alert('Choose Computer First Move [Game Type]');
        return;
      }
    }
    // previous selection must choose direction
    const must_choose = this.state.must_choose;
    const selected = this.state.selected;
    const boardstate = this.getCurrentState();
    const visited = this.state.visited;
    let movetype, possible_move, must_capture;
    // eslint-disable-next-line
    let capture_backward, capture_forward, was_capture;
    const has_moved = this.state.has_moved;
    /* if no piece was selected:
      - return if the next selected is not my_pieces
      - else: check if the selected piece can move and return available move
    */

    if (must_choose.length > 1){
      if (!(must_choose.includes(i))){
        alert("You must choose between "+utils.ToSquare(must_choose[0])+' and '+utils.ToSquare(must_choose[1]));
        return
      } else {
        const new_pos = this.state.new_pos;
        const newboard = utils.makeMove_choosen(boardstate, selected, new_pos, i);
        if (this.check_winner(newboard)){
          this.setState({visited:[], computer_move: false});
          return
        }
        if (!(has_moved)){
          visited.push(selected);
        }
        visited.push(new_pos);
        possible_move = utils.legalMove(newboard, new_pos, visited, true);
        if (possible_move.length  > 0){
          this.setState({history: this.state.history.concat([{
            boardState: newboard, currentPlayer: true,}]),
            must_choose: [], 
            selected: new_pos,
            visited: visited,
            available_move: possible_move,
            has_moved: true,
            step_number: this.state.history.length,
          });
        return;
        } else{
          this.resetState(newboard, true);
          return;
        }
      }
    }


    must_capture = utils.MustCapture(boardstate, this.state.has_moved);

    const available_move = this.state.available_move;
    
    // if clicked the selected piece twice undo selection
    if ((selected === i) && (!(has_moved))) {
      this.setState({selected: null, available_move: []});
      return;
    }
    if ((selected) && (boardstate[i] === 'one') && (!(has_moved))){
      possible_move = utils.legalMove(boardstate, i, visited, must_capture);
      if (possible_move.length > 0){
        this.setState({selected: i, available_move: possible_move});
      } else {
       return
      }
    }


    /* No pieces selected */
    if (!(selected) && (! (this.state.computer_move))){
      if (boardstate[i] !== 'one'){
        return
      } else {
        possible_move = utils.legalMove(boardstate, i, visited, must_capture);
        
        // if it can move mark it as selected and show available move
        if (possible_move.length > 0){
           this.setState({selected: i, available_move: possible_move});
        } else{
          return
        }
      }
    }

    if (available_move.includes(i)){
      movetype = i - selected;
      // Check if both forward and backward direction are possible
      capture_forward = selected + 2*movetype;
      capture_backward = selected - movetype;

      if ((boardstate[capture_forward] ==='two') && (boardstate[capture_backward] ==='two')){
        this.setState({must_choose: [capture_forward, capture_backward], new_pos:i});
        alert("Choose between "+utils.ToSquare(capture_forward)+' and '+utils.ToSquare(capture_backward));
        return
      }

      const newboard1 = utils.makeMove(boardstate, selected, i, movetype);
      if (this.check_winner(newboard1)){
        this.setState({visited:[], computer_move: false});
        return
      }
      if (!(has_moved)){
        visited.push(selected);
      }
      visited.push(i);
      if (!must_capture){
        this.resetState(newboard1, true);
        return;
        // this.resetState(result.boardstate);
      }

      
      possible_move = utils.legalMove(newboard1, i, visited, must_capture);
      if (possible_move.length>=1){
        this.setState({history: this.state.history.concat([{
          boardState: newboard1, 
          currentPlayer: true,}]),
        selected: i, 
        available_move: possible_move,
        has_moved: true,
        visited: visited,
        must_choose: [],
        step_number: this.state.history.length,});
      } else{
          this.resetState(newboard1, true);
          return;
      }
    }
  }
  

  render() {
    
    // const status = this.status;

    const boardstate = this.getCurrentState();
    const selected = this.state.selected;
    const available_move = this.state.available_move;
    const must_choose = this.state.must_choose; 
    this.check_winner(boardstate);

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



class MoveStatus extends React.Component {
  renderTableData() {
    const move_str = this.props.move_string;
    return move_str.map((history, index) => {
        const {turn, human, computer } = history //destructuring
        return (
          <tr key={turn}>
             <td style={{textAlign:'center'}}>{turn}</td>
             <td>{human}</td>
             <td>{computer}</td>
          </tr>
        )
    })
 }
  render(){
    const status = this.props.status;
    return (
      <div className="box_status">
      <Container fluid={true} className="status_show">
        {/* <Row noGutters={true} style={{fontWeight: 'bold'}}>Game Status</Row> */}
        <h3>Game Status</h3>
        <Row noGutters={true} className="game_status">
          <Col className="col-centered" id="log_status" >
            <div className="center-me" id="statusbox"> {status}
            </div>
          </Col>
        </Row>
        {/* <Row noGutters={true} style={{fontWeight: 'bold'}}> Moves</Row>  */}
        <h3>Moves</h3>
        <Row noGutters={true} className="moves_log">
          <Col className="moves_tables">
            <div id="statusall">
              <table id='moves' style={{width:'100%'}}>
                <thead>
                <tr style={{borderBottom:'1px dashed', borderCollapse:'collapse'}}>
                    <th width="20%" style={{textAlign:'center'}}>ID</th>
                    <th width="40%">Human</th>
                    <th width="40%">Computer</th>
                  </tr>
                </thead>
                <tbody>
                    {this.renderTableData()}
                </tbody>
              </table>
            </div>
          </Col>
        </Row>              
      </Container>
    </div>
    )
}
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
      <div className="rowcross" >
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
  winner: false,
  history_turn: [{
    boardState: utils.create_board(346553855, 562399296880640),
    turn_id: 0,
    human:'',
    computer:'',
  }],
  turn_number: 0,
};


export default App;
