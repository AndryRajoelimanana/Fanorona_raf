class Board extends React.Component {
  constructor(props) {
    super(props);
    
    this.calcPoints = this.calcPoints.bind(this);
    
    this.state = {
      width: 20,
      height: 15,
      points: [],
    };    
  }
  
  componentWillMount() {
    this.calcPoints(
      this.state.width, this.state.height
    );
  }


  calcPoints = (width, height) => {
    
    const points = [];
    points.push([width/20, height/12]);
    points.push([width/20, height - height/12]);
    
    this.setState({
        points
    });
  };

  render() {
    return (
      <div className='Boardsvg'>
        <Svg
          points={this.state.points}
          width={this.state.width}
          height={this.state.height}
        />
      </div>
    )
  }
};

const Svg = ({
  points,
  width,
  height,
}) => {
  return (
    <svg
      className='Svg'
      viewBox={`0 0 ${height} ${width}`}
      xmlns='http://www.w3.org/2000/svg'
    >
    <Polygon points={points}/>
  </svg>
  )
};

const Polygon = ({
  points,
}) => {
  const poinstData = points.join(' ');

  return (
    <polygon className='polygon' points={poinstData}/>
  )
}

ReactDOM.render(
  <Board />,
  document.getElementById('root1')
)
