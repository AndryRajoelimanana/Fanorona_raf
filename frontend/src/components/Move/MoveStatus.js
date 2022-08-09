import React from 'react';
import { Container, Row, Col} from 'react-bootstrap';


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

export default MoveStatus;