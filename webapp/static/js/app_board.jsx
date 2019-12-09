class Square extends React.Component {
render() {
    return (
    <button className="square">
        {/* TODO */}
    </button>
    );
}
}

class Diamond extends React.Component {
    render() {
        return (
        <button className="diamond">
            {/* TODO */}
        </button>
        );
    }
    }


class Board extends React.Component {
renderSquare(i) {
    return <Square />;
}
renderDiamond(i) {
    return <Diamond />;
}
render() {
    const status = 'Next player: X';

    return (
    <div>
        <div className="status">{status}</div>
        <div className="board-row">
        {this.renderSquare(0)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(1)}
        {this.renderDiamond(1)}

        </div>
        <div className="board-row">
        {this.renderSquare(3)}
        {this.renderSquare(4)}
        {this.renderSquare(5)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(1)}
        </div>

        <div className="board-row">
        {this.renderSquare(6)}
        {this.renderSquare(7)}
        {this.renderSquare(8)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(1)}
        </div>
        <div className="board-row">
        {this.renderSquare(6)}
        {this.renderSquare(7)}
        {this.renderSquare(8)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(1)}
        </div>

    </div>
    );
}
}

class Game extends React.Component {
render() {
    return (
    <div className="game">
        <div className="game-board">
        <Board />
        </div>
        <div className="game-info">
        <div>{/* status */}</div>
        <ol>{/* TODO */}</ol>
        </div>
    </div>
    );
}
}

// ========================================

ReactDOM.render(
<Game />,
document.getElementById('root')
);
