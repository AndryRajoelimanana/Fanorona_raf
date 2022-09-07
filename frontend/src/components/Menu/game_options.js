import React from 'react';
import { Form, Row, Col } from 'react-bootstrap';


export function GameMenu(props) {
  return (
    <Row>
    <Col xs={12} sm={12} md={8}>
      <Form className='form_command'>
          <Form.Row className="justify-content-md-center">
            <MoveFirst move_first={props.move_first} onChange={props.handle_move_first}/>
            <GameType disabled_game={props.disabled_game} game_type={props.game_type} onChange={props.handle_game_type} />
            <SearchDepth depth={props.depth} onChange={props.handle_depth}/>
            <SearchDepth1 depth={props.maxtime} onChange={props.handle_maxtime}/>
          </Form.Row>
      </Form>
    </Col>
    </Row>
  );
}


export function MoveFirst(props) {
  const move_first = props.move_first;
  return (
    <Form.Group as={Col} md="3" xs="3" controlId="opponent">
      <Form.Label>Move First</Form.Label>
      <Form.Control value={move_first} as="select" onChange={props.onChange}>
          <option value="computer">Computer</option>
          <option value="human">Human</option>
      </Form.Control>
    </Form.Group>
  );
}


export function GameType(props) {
  const disabled_game = props.disabled_game;
  const game_type = props.game_type;
  
  return (
    <Form.Group as={Col} md="3" xs="3" controlId="move_first">
      <Form.Label>GameType</Form.Label>
      <Form.Control disabled={disabled_game}  value={game_type} as="select" onChange={props.onChange} >
        <option value="vakyloha">Vaky loha</option>
        <option value="kobana">Kobana</option>
        <option value="fohy">Fohy</option>
        <option value="havia">Havia</option>
        <option value="havanana">Havanana</option>
      </Form.Control>
    </Form.Group>
  );
}


export function SearchDepth(props) {
  const depth = props.depth;
  return (
    <Form.Group as={Col} md="3" xs="3" controlId="move_first">
      <Form.Label>Depth</Form.Label>
      <Form.Control value={depth} as="select"  onChange={props.onChange}>
        <option>1</option>
        <option>2</option>
        <option>3</option>
        <option>4</option>
        <option>5</option>
      </Form.Control>
    </Form.Group>
  );
}

export function SearchDepth1(props) {
  const depth = props.depth;
  return (
    <Form.Group as={Col} md="3" xs="3" controlId="move_first">
      <Form.Label>MaxTime</Form.Label>
      <Form.Control value={depth} as="select"  onChange={props.onChange}>
        <option>1000</option>
        <option>3000</option>
        <option>5000</option>
        <option>8000</option>
        <option>10000</option>
      </Form.Control>
    </Form.Group>
  );
}


export default GameMenu;