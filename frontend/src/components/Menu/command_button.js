import React from "react"

export default function GameOptionsBar(props){
  return (
    <div className="command_button" id="game-options-bar">
      <button   className="game_button vertical_center"
        onClick={() => {props.createNewGame()}}
        >Restart</button>
      <button className="game_button vertical_center"
        onClick={() => {props.passgame()}}
        >Pass</button>
      <button className="game_button vertical_center"
        onClick={() => {props.undogame()}}
        >Undo</button>
    </div>
  )
}