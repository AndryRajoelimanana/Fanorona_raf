(this["webpackJsonpmy-app"]=this["webpackJsonpmy-app"]||[]).push([[0],{104:function(e,t,n){e.exports=n(270)},109:function(e,t,n){},110:function(e,t,n){},270:function(e,t,n){"use strict";n.r(t);var o=n(0),a=n.n(o),s=n(99),r=n.n(s),i=(n(109),n(100)),l=n(28),c=n(29),u=n(31),m=n(30),h=n(27),d=n(32);n(110);function v(e,t){for(var n=Array(50).fill("none"),o=e.toString(2).padStart(64,"0"),a=t.toString(2).padStart(64,"0"),s=o.length,r=a.length,i=0;i<50;i++)"1"===o.charAt(s-i)?n[i]="one":"1"===a.charAt(r-i)?n[i]="two":n[i]="none";return n}function w(e){return{0:"e",1:"d",2:"c",3:"b",4:"a"}[~~(e/10)]+(10-e%10)}function _(e){for(var t=0;t<e.length;t++)if(0===t)var n=w(e[t]);else n=n+"-"+w(e[t]);return n}function p(e,t,n,o){var a,s,r=[];a=t%2!==~~(t/10)%2?[-11,-10,-9,-1,1,9,10,11]:[-10,-1,1,10];for(var i=0;i<a.length;i++){var l=t+a[i];if(l%10!==0&&(("none"===e[l]||"none eaten"===e[l])&&!n.includes(l)))if(o){var c=n.length;if(c>1){var u=n[c-2];s=n[c-1]-u}else s=0,0;f(e,t,a[i])&&a[i]!==s&&r.push(l)}else r.push(t+a[i])}return r}function f(e,t,n){return"two"===e[t+2*n]||"two"===e[t-n]}function b(e,t){return!!t||function(e){for(var t=e.reduce((function(e,t,n){return"one"===t?e.concat(n):e}),[]),n=[],o=0;o<t.length;o++)if(p(e,t[o],n,!0).length>=1)return!0;return!1}(e)}function S(e){var t;return"vakyloha"===e?t=["none","one","one","one","one","none eaten","one","one","one","one","none","one","one","one","one","none eaten","one","one","one","one","none","one","two","one","two","two","one","two","one","two","none","two","two","two","two","none","two","two","two","two","none","two","two","two","two","two","two","two","two","two"]:"kobana"===e?t=["none","one","one","one","one","one","one","one","one","one","none","one","one","one","one","one","one","one","one","one","none","one","two","none eaten","none","two","one","two","one","two","none","two","two","two","two","two","two","two","two","two","none","two","two","two","two","two","two","two","two","two"]:"fohy"===e?t=["none","one","one","one","one","one","one","one","one","one","none","one","one","one","one","one","one","one","one","one","none","one","two","one","none","two","none eaten","two","one","two","none","two","two","two","two","two","two","two","two","two","none","two","two","two","two","two","two","two","two","two"]:"havia"===e?t=["none","one","one","none eaten","one","one","one","one","one","one","none","one","one","one","none eaten","one","one","one","one","one","none","one","two","one","two","two","one","two","one","two","none","two","two","two","two","two","none","two","two","two","none","two","two","two","two","two","two","two","two","two"]:"havanana"===e&&(t=["none","one","one","one","one","one","one","none eaten","one","one","none","one","one","one","one","one","none eaten","one","one","one","none","one","two","one","two","two","one","two","one","two","none","two","two","two","none","two","two","two","two","two","none","two","two","two","two","two","two","two","two","two"]),t}var g=n(101),y=n.n(g),E=n(272),R=n(273),C=n(103),k=n(274),N=(n(128),function(e){function t(e){var n;return Object(l.a)(this,t),(n=Object(u.a)(this,Object(m.a)(t).call(this,e))).restart_board=function(){n.setState(n.initialState),console.log("gg",Object(h.a)(n))},n.componentDidUpdate=function(e,t){n.state.computer_move&&(n.setState({is_moving:!0}),setTimeout((function(){n.wait_computer()}),1e3),n.setState({computer_move:!1,is_moving:!1}))},n.undo_move=function(){var e,t,o,a=n.state.turn_number;a<=2?n.restart_board():(a%2===0?(e=n.state.history_turn[a-2].step_number,t=n.state.history.slice(0,e+1),o=n.state.history_turn.slice(0,a-1),a-=1):(e=n.state.history_turn[a-1].step_number,o=n.state.history_turn.slice(0,a),t=n.state.history.slice(0,e+1)),n.setState({history:t,history_turn:o,selected:null,available_move:[],visited:[],must_choose:[],new_pos:null,step_number:e,turn_number:a-1}))},n.resetState=function(e){var t,o=function(e){for(var t=0,n=0,o=0;o<50;o++)"one"===e[o]?++t:"two"===e[o]&&++n;return 0===t?"Computer WIN":0===n?"You WIN":null}(e);if(o)return alert("game over: "+o),void n.restart_board();var a=_(n.state.visited),s=n.state.turn_number+1;if(0===s)switch(a){case"d5-c5":"vakyloha";break;case"c4-c5":"none eaten"===e[27]?"kobana":"none eaten"===e[24]&&"fohy";break;case"d4-c5":"havanana";break;case"d6-c5":"havia"}var r=n.AppendHistory({boardState:e,step_number:n.state.history.length,turn_id:s,human:a,computer:""});t=!!e.includes("none eaten"),n.setState((function(o){return Object(i.a)({history:n.state.history.concat([{boardState:e}]),selected:null,computer_move:!1,available_move:[],visited:[],has_moved:!1,must_choose:[],step_number:n.state.history.length,status:"Computer is moving",history_turn:r,turn_number:s,was_capture:t},"computer_move",!o.computer_move)}))},n.pass_game=function(){if(n.state.has_moved){var e=_(n.state.visited),t=n.state.turn_number+1,o=n.getCurrentState(),a=n.AppendHistory({boardState:o,step_number:n.state.history.length,turn_id:t,human:e,computer:""});n.setState({was_capture:!0,computer_move:!0,selected:null,status:"Computer is moving",available_move:[],visited:[],has_moved:!1,must_choose:[],history_turn:a,turn_number:t})}},n.handle_game_type=function(e){var t=e.target.value;n.restart_board(),n.setState({history:[{boardState:S(t)}],history_turn:[{boardState:S(t),turn_id:0,human:"",computer:""}],game_type:t,status:"human to move"})},n.handle_move_first=function(e){n.restart_board(),n.setState({move_first:e.target.value})},n.handle_depth=function(e){n.setState({depth:e.target.value})},n.onClick=function(e){if(!n.state.computer_move)if("computer"!==n.state.move_first||n.state.status){var t,o,a,s,r,i=n.state.must_choose,l=n.state.selected,c=n.getCurrentState(),u=n.state.visited,m=n.state.has_moved;if(i.length>1){if(i.includes(e)){var h=n.state.new_pos,d=function(e,t,n,o){var a,s,r=n-t;for(t+2*r===o?s=n+(a=r):t-r===o&&(s=n+2*(a=-r)),(e=e.map((function(e){return"none eaten"===e?"none":e})))[t]="none",e[n]="one";"two"===e[s];)e[s]="none eaten",s+=a;return e}(c,l,h,e);return m||u.push(l),u.push(h),(o=p(d,h,u,!0)).length>0?void n.setState({history:n.state.history.concat([{boardState:d,currentPlayer:!0}]),must_choose:[],selected:h,visited:u,available_move:o,has_moved:!0,step_number:n.state.history.length}):void n.resetState(d)}alert("You must choose between "+w(i[0])+" and "+w(i[1]))}else{a=b(c,n.state.has_moved);var v=n.state.available_move;if(l!==e||m){if(l&&"one"===c[e]&&!m){if(!((o=p(c,e,u,a)).length>0))return;n.setState({selected:e,available_move:o})}if(!l&&!n.state.computer_move){if("one"!==c[e])return;if(!((o=p(c,e,u,a)).length>0))return;n.setState({selected:e,available_move:o})}if(console.log("tato21"),v.includes(e)){if(s=l-(t=e-l),"two"===c[r=l+2*t]&&"two"===c[s])return n.setState({must_choose:[r,s],new_pos:e}),void alert("Choose between "+w(r)+" and "+w(s));var _=function(e,t,n,o){var a,s;for("two"===(e=e.map((function(e){return"none eaten"===e?"none":e})))[t+2*o]?s=n+(a=o):"two"===e[t-o]&&(s=n+2*(a=-o)),e[t]="none",e[n]="one";"two"===e[s];)e[s]="none eaten",s+=a;return e}(c,l,e,t);if(m||u.push(l),u.push(e),console.log("teto available"),!a)return void n.resetState(_);if(!((o=p(_,e,u,a)).length>=1))return void n.resetState(_);n.setState({history:n.state.history.concat([{boardState:_,currentPlayer:!0}]),selected:e,available_move:o,has_moved:!0,visited:u,must_choose:[],step_number:n.state.history.length})}}else n.setState({selected:null,available_move:[]})}}else alert("Choose Computer First Move [Game Type]")},n.initialState={history:[{boardState:v(173538815,562399469895680)}],selected:null,step_number:0,has_moved:null,available_move:[],visited:[],must_choose:[],computer_move:!1,is_moving:!1,was_capture:!1,status:null,depth:3,game_type:null,move_first:"human",winner:!1,history_turn:[{boardState:[],turn_id:0,human:"",computer:""}],turn_number:0},n.state=n.initialState,n}return Object(d.a)(t,e),Object(c.a)(t,[{key:"computer_turn",value:function(e,t,n){var o=this,a={boardstate:e,was_capture:t,depth:n},s=[],r=[];y.a.post("/pass",a).then((function(t){for(var n,a=t.data.move_log,i=t.data.movedict,l=a[0],c=0;c<a.length;c++){n=a[c],e=e.map((function(e){return"none eaten"===e?"none":e}));for(var u=i[n],m=0;m<u.length;m++)e[u[m]]="none eaten";s=s.concat([n]),e[l]="none",e[l=n]="two",r=r.concat([e])}o.iterate_move(s,r,[])})).catch((function(e){alert(e)}))}},{key:"iterate_move",value:function(e,t,n){var o=this,a=e.shift(),s=t.shift();n.push(a),0!==e.length?(this.setState({history:this.state.history.concat([{boardState:s}]),selected:a,step_number:this.state.history.length,visited:n}),setTimeout((function(){o.iterate_move(e,t,n)}),1e3)):this.resetState(s)}},{key:"wait_computer",value:function(){console.log("tato_wait_computer"),console.log(this.state);var e=this.getCurrentState(),t=this.state.was_capture,n=this.state.depth;this.computer_turn(e,t,n)}},{key:"getCurrentState",value:function(){var e=this.state.history.slice();return e.length>1?e[e.length-1].boardState:e[0].boardState}},{key:"AppendHistory",value:function(e){return this.state.history_turn.slice().concat([e])}},{key:"render",value:function(){var e,t=this,n=this.getCurrentState(),o=this.state.selected,s=this.state.available_move,r=this.state.must_choose;e=this.state.is_moving?"Computer is moving...":r.length?"Choose: "+w(r[0])+" or "+w(r[1]):o?"Piece selected: "+w(o):"Human to move";var i=function(e){for(var t=[],n=e.length,o=0;o<n;o++)o%2===0?t.push({turn:o/2+1,human:e[o].human,computer:" "}):t[t.length-1].computer=e[o].human;return t}(this.state.history_turn.slice(1)),l="human"===this.state.move_first;return n||this.restart_board(),a.a.createElement("div",{className:"main"},a.a.createElement(E.a,{fluid:!0,id:"container1"},a.a.createElement(R.a,{noGutters:!0},a.a.createElement(C.a,{xs:12,sm:12,md:8},a.a.createElement(k.a,{className:"form_command"},a.a.createElement(k.a.Row,{className:"justify-content-md-center"},a.a.createElement(k.a.Group,{as:C.a,md:"3",xs:"4",controlId:"opponent"},a.a.createElement(k.a.Label,null,"Move First"),a.a.createElement(k.a.Control,{value:"human",as:"select",onChange:this.handle_move_first},a.a.createElement("option",{value:"computer"},"Computer"),a.a.createElement("option",{value:"human"},"Human"))),a.a.createElement(k.a.Group,{as:C.a,md:"3",xs:"4",controlId:"move_first"},a.a.createElement(k.a.Label,null,"Game Type"),a.a.createElement(k.a.Control,{disabled:l,value:this.state.game_type,as:"select",onChange:this.handle_game_type},a.a.createElement("option",{value:"vakyloha"},"Vaky loha"),a.a.createElement("option",{value:"kobana"},"Kobana"),a.a.createElement("option",{value:"fohy"},"Fohy"),a.a.createElement("option",{value:"havia"},"Havia"),a.a.createElement("option",{value:"havanana"},"Havanana"))),a.a.createElement(k.a.Group,{as:C.a,md:"3",xs:"4",controlId:"depth"},a.a.createElement(k.a.Label,null,"Depth"),a.a.createElement(k.a.Control,{value:this.state.depth,as:"select",onChange:this.handle_depth},a.a.createElement("option",null,"1"),a.a.createElement("option",null,"2"),a.a.createElement("option",null,"3"),a.a.createElement("option",null,"4"),a.a.createElement("option",null,"5"))))))),a.a.createElement(R.a,{noGutters:!0},a.a.createElement("div",{className:"windowa"},a.a.createElement(R.a,{noGutters:!0},a.a.createElement(C.a,{xs:12,sm:12,md:8,className:"game_windows row-eq-height"},a.a.createElement("div",{className:"aspect_ratiodiv"},a.a.createElement(E.a,{fluid:!0,className:"BoardCont"},a.a.createElement(R.a,{noGutters:!0,className:"crosscont"},a.a.createElement("div",{className:"aspect_ratiodiv1"},a.a.createElement(x,{boardstate:n,selected:o,available_move:s,onClick:function(e){return t.onClick(e)}}))),a.a.createElement(R.a,{noGutters:!0,className:"command_button"},a.a.createElement(C.a,{style:{textAlign:"center"}},a.a.createElement("button",{className:"game_button",onClick:function(){return t.restart_board()}},"Restart")),a.a.createElement(C.a,{style:{textAlign:"center"}},a.a.createElement("button",{className:"game_button",onClick:function(){return t.pass_game()}},"Pass")),a.a.createElement(C.a,{style:{textAlign:"center"}},a.a.createElement("button",{className:"game_button",onClick:function(){return t.undo_move()}},"Undo")))))),a.a.createElement(C.a,{xs:12,sm:12,md:4,className:"status_window row-eq-height"},a.a.createElement(O,{status:e,move_string:i})))))))}}]),t}(a.a.Component)),j=function(e){var t=e.id,n=w(t),o=e.selected,s=e.available,r="player-"+e.stoneClasses+" "+n;return t===o&&(r+="  selected"),s.indexOf(t)>-1&&(r+="  available"),a.a.createElement("div",{className:r,id:t,onClick:e.onClick})},O=function(e){function t(){return Object(l.a)(this,t),Object(u.a)(this,Object(m.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(c.a)(t,[{key:"renderTableData",value:function(){return this.props.move_string.map((function(e,t){var n=e.turn,o=e.human,s=e.computer;return a.a.createElement("tr",{key:n},a.a.createElement("td",{style:{textAlign:"center"}},n),a.a.createElement("td",null,o),a.a.createElement("td",null,s))}))}},{key:"render",value:function(){var e=this.props.status;return a.a.createElement("div",{className:"box_status"},a.a.createElement(E.a,{fluid:!0,className:"status_show"},a.a.createElement("h3",null,"Game Status"),a.a.createElement(R.a,{noGutters:!0,className:"game_status"},a.a.createElement(C.a,{className:"col-centered",id:"log_status"},a.a.createElement("div",{className:"center-me",id:"statusbox"}," ",e))),a.a.createElement("h3",null,"Moves"),a.a.createElement(R.a,{noGutters:!0,className:"moves_log"},a.a.createElement(C.a,{className:"moves_tables"},a.a.createElement("div",{id:"statusall"},a.a.createElement("table",{id:"moves",style:{width:"100%"}},a.a.createElement("thead",null,a.a.createElement("tr",{style:{borderBottom:"1px dashed",borderCollapse:"collapse"}},a.a.createElement("th",{width:"20%",style:{textAlign:"center"}},"ID"),a.a.createElement("th",{width:"40%"},"Human"),a.a.createElement("th",{width:"40%"},"Computer"))),a.a.createElement("tbody",null,this.renderTableData())))))))}}]),t}(a.a.Component),x=function(e){function t(){var e,n;Object(l.a)(this,t);for(var o=arguments.length,s=new Array(o),r=0;r<o;r++)s[r]=arguments[r];return(n=Object(u.a)(this,(e=Object(m.a)(t)).call.apply(e,[this].concat(s)))).RenderStones=function(e){var t=n.props.boardstate[e],o=n.props.selected,s=n.props.available_move;return a.a.createElement(j,{stoneClasses:t,id:e,selected:o,available:s,onClick:function(){return n.props.onClick(e)}})},n}return Object(d.a)(t,e),Object(c.a)(t,[{key:"render",value:function(){return a.a.createElement("div",{className:"rowcross"},a.a.createElement("div",{className:"crossed"},this.RenderStones(49),this.RenderStones(48),this.RenderStones(39),this.RenderStones(38)),a.a.createElement("div",{className:"crossed"},this.RenderStones(47),this.RenderStones(46),this.RenderStones(37),this.RenderStones(36)),a.a.createElement("div",{className:"crossed"},this.RenderStones(45),this.RenderStones(44),this.RenderStones(35),this.RenderStones(34)),a.a.createElement("div",{className:"crossed_left"},this.RenderStones(43),this.RenderStones(42),this.RenderStones(41),this.RenderStones(33),this.RenderStones(32),this.RenderStones(31)),a.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(29),this.RenderStones(28),this.RenderStones(19),this.RenderStones(18),this.RenderStones(9),this.RenderStones(8)),a.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(27),this.RenderStones(26),this.RenderStones(17),this.RenderStones(16),this.RenderStones(7),this.RenderStones(6)),a.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(25),this.RenderStones(24),this.RenderStones(15),this.RenderStones(14),this.RenderStones(5),this.RenderStones(4)),a.a.createElement("div",{className:"crossed_bottom_left"},this.RenderStones(23),this.RenderStones(22),this.RenderStones(21),this.RenderStones(13),this.RenderStones(12),this.RenderStones(11),this.RenderStones(3),this.RenderStones(2),this.RenderStones(1)))}}]),t}(a.a.Component),G=(v(173538815,562399469895680),v(173538815,562399469895680),N);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));n(269);r.a.render(a.a.createElement(G,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[104,1,2]]]);
//# sourceMappingURL=main.2eab6842.chunk.js.map