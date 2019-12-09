class App extends React.Component {
  constructor(props) {
    super(props);
    
    this.handleChange = this.handleChange.bind(this);
    this.calcPoints = this.calcPoints.bind(this);
    
    this.state = {
      vertices: 3,
      circleRadius: 3,
      size: 400,
      showVertexDots: true,
      showVertexLines: true,
      points: [],
    };    
  }
  
  componentWillMount() {
    this.calcPoints(
      this.state.circleRadius, this.state.size, this.state.vertices
    );
  }
  
  handleChange = (event) => {
    this.setState({
      vertices: event.target.value
    });
    
    this.calcPoints(
      this.state.circleRadius, this.state.size, event.target.value
    );
  };

  handleVertexCheckbox = () => {
    const showVertexDots = !this.state.showVertexDots;
    this.setState({
      showVertexDots
    });
  };

  handleLineCheckbox = () => {
    const showVertexLines = !this.state.showVertexLines;
    this.setState({
      showVertexLines
    });
  };

  calcPoints = (circleRadius, size, vertices) => {
    const RAD = Math.PI / 180;
    const TWO_PI = Math.PI * 2;
    const points = [];
    const radius = (size/2) - circleRadius;
    const center = radius + circleRadius;
    const theta = TWO_PI / vertices;
    const angle = RAD * -90;

    for(var i = 0; i < vertices; i++) {
      let x = radius * Math.cos(theta * i + angle) + center;
      let y = radius * Math.sin(theta * i + angle) + center;
      points.push([x, y]);
    }
    
    this.setState({
        points
    });
  };

  render() {
    return (
      <div className='App-wrapper'>
        <Svg
          circleRadius={this.state.circleRadius}
          points={this.state.points}
          showVertexDots={this.state.showVertexDots}
          showVertexLines={this.state.showVertexLines}
          width={this.state.size}
          height={this.state.size}
        />
        
        <div className='Controls'>
          <Checkbox
            trueLabel='Show Lines'
            falseLabel='Hide Lines'
            checked={this.state.showVertexLines}
            onChange={this.handleLineCheckbox}
          />
          <Checkbox
            trueLabel='Show Dots'
            falseLabel='Hide Dots'
            checked={this.state.showVertexDots}
            onChange={this.handleVertexCheckbox}
          />        
          <div className='Controls-slider-wrap'>
            <input
              type='range'
              min='3'
              max='100'
              onChange={this.handleChange}
              value={this.state.vertices}
            />
            <p className='Controls-slider-label'>{this.state.vertices} </p>
          </div>
        </div>
      </div>
    )
  }
};

const Svg = ({
  circleRadius,
  points,
  showVertexDots,
  showVertexLines,
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

    { showVertexLines ?
      points.map((point, i) => 
       <VertexLine key={i} point={point} radius={width} />
      )
    : null }

    { showVertexDots ?
      points.map((point, i) =>
       <VertexDot circleRadius={circleRadius} key={i} point={point} radius={width} />
      )
    : null }
  </svg>
  )
};

const Checkbox = ({
  checked,
  trueLabel,
  falseLabel,
  onChange,
  value,
}) => {
  return(
    <label className='Checkbox'>
      <input
        className='Checkbox--checkbox'
        type='checkbox'
        value={trueLabel}
        checked={checked}
        onChange={onChange}
      />
      <span className='Checkbox--label'>{checked ? falseLabel : trueLabel}</span>
    </label>
  )
}

const VertexDot = ({
  circleRadius,
  point
}) => {
  return(
    <circle
      cx={point[0]}
      cy={point[1]}
      r={circleRadius}
      className='circle'
    />
  )
}

const VertexLine = ({
  point,
  radius
}) => {
  const centerX = radius / 2;
  const centerY = radius / 2;
  return(
    <line
      x1={centerX}
      y1={centerY}
      x2={point[0]}
      y2={point[1]}
      className='App-line'
    />
  )
}

const Polygon = ({
  points,
  width,
}) => {
  const poinstData = points.join(' ');

  return (
    <polygon className='polygon' points={poinstData} />
  )
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
)
