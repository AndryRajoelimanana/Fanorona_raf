import React from 'react';
import { Container, Row, Col} from 'react-bootstrap';
import ClockLoader from "react-spinners/ClockLoader";
import {useEffect, useState} from 'react';
// import { CountdownCircleTimer } from "react-countdown-circle-timer";


class MoveStatus extends React.Component {

  render(){
    const status = this.props.status;
    return (
      // <div className="box_status">
        <Container fluid={true} className="status_show">
          {/* <Row noGutters={true} style={{fontWeight: 'bold'}}>Game Status</Row> */}
          <h3>Game Status</h3>
            <GameStatus status={status}/>
          <h3>Moves</h3>
            <MoveLog move_string={this.props.move_string}/>
        </Container>
    // </div>
    )
}
}



function RenderTables(props) {
  const move_str = props.move_string;
  return move_str.map((history) => {
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

function getWindowSize() {
  const {innerWidth, innerHeight} = window;
  return {innerWidth, innerHeight};
}


// const renderTime = ({ remainingTime }) => {
//   if (remainingTime === 0) {
//     return <div className="timer">Too lale...</div>;
//   }
//   return (
//     <div className="timer">
//       <div className="text">Remaining</div>
//       <div className="value">{remainingTime}</div>
//       <div className="text">seconds</div>
//     </div>
//   );
// };


function SpinLoader(props) {
  const [windowSize, setWindowSize] = useState(getWindowSize());
  useEffect(() => {
    function handleWindowResize() {
      setWindowSize(getWindowSize());
    }
    window.addEventListener('resize', handleWindowResize);
    return () => {
      window.removeEventListener('resize', handleWindowResize);
    };
  }, []);


  return (
    <Row className="center-me loading_status">
      <Col xs={1} lg={1} md={1} className="loading_col">
      </Col>
      <Col xs={3} lg={3} md={3} className="loading_col">
      {/* <CountdownCircleTimer
          key={0}
          isPlaying
          duration={10}
          colors={[["#004777", 0.33], ["#F7B801", 0.33], ["#A30000"]]}
          onComplete={() => [true, 1000]}
        >
          {renderTime}
      </CountdownCircleTimer> */}
        <ClockLoader className="searching" loading={true} cssOverride={{"position":"absolute"}} color={"#000000"} size={windowSize.innerWidth/25} />
      </Col>
      <Col xs={8} lg={8} md={8} className="loading_col">
        <div className="searching var_font">AI searching</div>
      </Col>
    </Row>
  );
}


function GameStatus(props) {
  const status = props.status;
  const isloading = status === 'AI is searching...';
  // const isloading =true;
  return (
    <Row className="game_status">
        <Col>
          <div id="log_status" >
            {isloading ?  <SpinLoader/> : <div className="center-me" id="statusbox">{status}</div>}
          </div>
        </Col>
    </Row>
  );
}

function MoveLog(props) {
  return (
    <Row className="moves_log">
        <div className="moves_tables" >
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
                <RenderTables move_string={props.move_string} />
            </tbody>
          </table>
        </div>
      </div>
    </Row>
  );
}


export default MoveStatus;