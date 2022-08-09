import React from 'react';
import {Form} from 'react-bootstrap';



const OptionMoveFirst = (props) => {
  const id = props.id;
  const idbox = ToSquare(id);
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



function Square(props) {
    return (
      <Form.Group as={Col} md="3" xs="4" controlId="opponent">
        <Form.Label>Move First</Form.Label>
        <Form.Control value={this.state.move_first} as="select" onChange={this.handle_move_first}>
            <option value="computer">Computer</option>
            <option value="human">Human</option>
        </Form.Control>
      </Form.Group>
  );
}


class GameOptions extends React.Component {
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

export default GameOptions;