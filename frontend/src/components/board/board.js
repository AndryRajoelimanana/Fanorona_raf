import React from 'react';
import { ToSquare } from './../../utils.js';


const Stones = (props) => {
  const id = props.id;
  const idbox = ToSquare(id);
  const selected = props.selected;
  const available = props.available;
  const choose = props.choose;
  const eaten = props.eaten;
  const turn_id = props.turn_id;
  var classname = "player-"+props.stoneClasses;
  if (id === selected){
    classname = classname + '  selected';
  }
  if (available.includes(id)) {
    classname = classname + '  available';
  }
  if (choose.includes(id)) {
    classname = classname + '  choose';
  }
  if (eaten.includes(id)) {
    if (turn_id % 2 === 0){
      classname = classname + ' eaten_one';
    } else{
      classname = classname + ' eaten_two';
    }
  }
  classname = classname +' '+idbox;
  return (
      <div className={classname} id={id} onClick={props
    .onClick}>
      </div>
  );
}


class BoardRender extends React.Component {

  RenderStones = (i) => {
    const stone = this.props.boardstate[i];
    const selected = this.props.selected;
    const available = this.props.available_move;
    const choose = this.props.choose;
    const eaten = this.props.eaten;
    const turn_id = this.props.turn_id;
    return (
      <Stones stoneClasses={stone.split(' ')[0]} id={i}  selected={selected}
  available={available} choose={choose} eaten={eaten} turn_id={turn_id}
  onClick={() => this.props.onClick(i)}
      />
  );
  }

  render() {
    // console.log(this.props.boardstate);
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


export default BoardRender;