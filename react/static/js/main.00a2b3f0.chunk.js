(this["webpackJsonpmy-app"]=this["webpackJsonpmy-app"]||[]).push([[0],{103:function(e,t,n){e.exports=n(269)},108:function(e,t,n){},109:function(e,t,n){},269:function(e,t,n){"use strict";n.r(t);var o=n(0),a=n.n(o),s=n(98),r=n.n(s),i=(n(108),n(27)),l=n(28),c=n(30),u=n(29),m=n(31);n(109);function h(e,t){for(var n=Array(50).fill("none"),o=e.toString(2).padStart(64,"0"),a=t.toString(2).padStart(64,"0"),s=o.length,r=a.length,i=0;i<50;i++)"1"===o.charAt(s-i)?n[i]="one":"1"===a.charAt(r-i)?n[i]="two":n[i]="none";return n}function d(e){return{0:"e",1:"d",2:"c",3:"b",4:"a"}[~~(e/10)]+(10-e%10)}function v(e){for(var t=0;t<e.length;t++)if(0===t)var n=d(e[t]);else n=n+"-"+d(e[t]);return n}function w(e,t,n,o){var a,s,r=[];a=t%2!==~~(t/10)%2?[-11,-10,-9,-1,1,9,10,11]:[-10,-1,1,10];for(var i=0;i<a.length;i++){var l=t+a[i];if(l%10!==0&&(("none"===e[l]||"none eaten"===e[l])&&!n.includes(l)))if(o){var c=n.length;if(c>1){var u=n[c-2];s=n[c-1]-u}else s=0,0;_(e,t,a[i])&&a[i]!==s&&r.push(l)}else r.push(t+a[i])}return r}function _(e,t,n){return"two"===e[t+2*n]||"two"===e[t-n]}function p(e,t){return!!t||function(e){for(var t=e.reduce((function(e,t,n){return"one"===t?e.concat(n):e}),[]),n=[],o=0;o<t.length;o++)if(w(e,t[o],n,!0).length>=1)return!0;return!1}(e)}function f(e){var t;return"vakyloha"===e?t=["none","one","one","one","one","none eaten","one","one","one","one","none","one","one","one","one","none eaten","one","one","one","one","none","one","two","one","two","two","one","two","one","two","none","two","two","two","two","none","two","two","two","two","none","two","two","two","two","two","two","two","two","two"]:"kobana"===e?t=["none","one","one","one","one","one","one","one","one","one","none","one","one","one","one","one","one","one","one","one","none","one","two","none eaten","none","two","one","two","one","two","none","two","two","two","two","two","two","two","two","two","none","two","two","two","two","two","two","two","two","two"]:"fohy"===e?t=["none","one","one","one","one","one","one","one","one","one","none","one","one","one","one","one","one","one","one","one","none","one","two","one","none","two","none eaten","two","one","two","none","two","two","two","two","two","two","two","two","two","none","two","two","two","two","two","two","two","two","two"]:"havia"===e?t=["none","one","one","none eaten","one","one","one","one","one","one","none","one","one","one","none eaten","one","one","one","one","one","none","one","two","one","two","two","one","two","one","two","none","two","two","two","two","two","none","two","two","two","none","two","two","two","two","two","two","two","two","two"]:"havanana"===e&&(t=["none","one","one","one","one","one","one","none eaten","one","one","none","one","one","one","one","one","none eaten","one","one","one","none","one","two","one","two","two","one","two","one","two","none","two","two","two","none","two","two","two","two","two","none","two","two","two","two","two","two","two","two","two"]),t}var b=n(100),S=n.n(b),g=n(271),y=n(272),E=n(102),R=n(273),C=(n(127),function(e){function t(e){var n;return Object(i.a)(this,t),(n=Object(c.a)(this,Object(u.a)(t).call(this,e))).restart_board=function(){n.setState(x)},n.componentDidUpdate=function(){n.state.computer_move&&(n.setState({is_moving:!0}),setTimeout((function(){n.wait_computer()}),1e3),n.setState({computer_move:!1,is_moving:!1}))},n.undo_move=function(){var e,t,o,a=n.state.turn_number;a<=2?n.restart_board():(a%2===0?(e=n.state.history_turn[a-2].step_number,t=n.state.history.slice(0,e+1),o=n.state.history_turn.slice(0,a-1),a-=1):(e=n.state.history_turn[a-1].step_number,o=n.state.history_turn.slice(0,a),t=n.state.history.slice(0,e+1)),n.setState({history:t,history_turn:o,selected:null,available_move:[],visited:[],must_choose:[],new_pos:null,step_number:e,turn_number:a-1}))},n.resetState=function(e){var t,o=v(n.state.visited),a=n.state.turn_number;if(0===a)switch(o){case"d5-c5":"vakyloha";break;case"c4-c5":"none eaten"===e[27]?"kobana":"none eaten"===e[24]&&"fohy";break;case"d4-c5":"havanana";break;case"d6-c5":"havia"}a+=1;var s={boardState:e,step_number:n.state.history.length,turn_id:a,human:o,computer:""};t=n.AppendHistory(s),n.setState({history:n.state.history.concat([{boardState:e}]),selected:null,computer_move:!1,available_move:[],visited:[],has_moved:!1,must_choose:[],step_number:n.state.history.length,status:"Computer is moving",history_turn:t,turn_number:a})},n.pass_game=function(){if(n.state.has_moved){var e=v(n.state.visited),t=n.state.turn_number+1,o={boardState:n.getCurrentState(),step_number:n.state.history.length,turn_id:t,human:e,computer:""};n.setState({was_capture:!0,computer_move:!0,selected:null,status:"Computer is moving",available_move:[],visited:[],has_moved:!1,must_choose:[],history_turn:n.AppendHistory(o),turn_number:t})}},n.handle_game_type=function(e){var t=e.target.value;n.restart_board(),n.setState({history:[{boardState:f(t)}],history_turn:[{boardState:f(t),turn_id:0,human:"",computer:""}],game_type:t,status:"human to move"})},n.handle_move_first=function(e){n.restart_board(),n.setState({move_first:e.target.value})},n.handle_depth=function(e){n.setState({depth:e.target.value})},n.onClick=function(e){if(console.log("tato"),!n.state.computer_move)if("computer"!==n.state.move_first||n.state.status){var t,o,a,s,r,i,l,c=n.state.must_choose,u=n.state.selected,m=n.getCurrentState(),h=n.state.visited,v=n.state.has_moved;if(c.length>1){if(c.includes(e)){var _=n.state.new_pos;return a=function(e,t,n,o){var a,s,r=n-t;for(t+2*r===o?s=n+(a=r):t-r===o&&(s=n+2*(a=-r)),(e=e.map((function(e){return"none eaten"===e?"none":e})))[t]="none",e[n]="one";"two"===e[s];)e[s]="none eaten",s+=a;return e}(m,u,_,e),v||h.push(u),h.push(_),(o=w(a,_,h,!0)).length>0?void n.setState({history:n.state.history.concat([{boardState:a,currentPlayer:!0}]),must_choose:[],selected:_,visited:h,available_move:o,has_moved:!0,step_number:n.state.history.length}):(n.resetState(a),void n.setState({was_capture:!0,selected:null,computer_move:!0,visited:[]}))}alert("You must choose between "+d(c[0])+" and "+d(c[1]))}else{console.log("tato1"),s=p(m,n.state.has_moved);var f=n.state.available_move;if(u!==e||v){if(u&&"one"===m[e]&&!v){if(!((o=w(m,e,h,s)).length>0))return;n.setState({selected:e,available_move:o})}if(!u&&!n.state.computer_move){if("one"!==m[e])return;if(o=w(m,e,h,s),console.log("tato2"),console.log(h),console.log(s),!(o.length>0))return;n.setState({selected:e,available_move:o})}if(console.log("tato2"),f.includes(e)){if(r=u-(t=e-u),"two"===m[i=u+2*t]&&"two"===m[r])return n.setState({must_choose:[i,r],new_pos:e}),void alert("Choose between "+d(i)+" and "+d(r));if(a=function(e,t,n,o){var a,s;for("two"===(e=e.map((function(e){return"none eaten"===e?"none":e})))[t+2*o]?s=n+(a=o):"two"===e[t-o]&&(s=n+2*(a=-o)),e[t]="none",e[n]="one";"two"===e[s];)e[s]="none eaten",s+=a;return e}(m,u,e,t),v||h.push(u),h.push(e),!s)return n.resetState(a),l=!!a.includes("none eaten"),void n.setState({was_capture:l,computer_move:!0,visited:[]});if(!((o=w(a,e,h,s)).length>=1))return n.resetState(a),l=!!a.includes("none eaten"),void n.setState({was_capture:l,computer_move:!0,visited:[]});n.setState({history:n.state.history.concat([{boardState:a,currentPlayer:!0}]),selected:e,available_move:o,has_moved:!0,visited:h,must_choose:[],step_number:n.state.history.length})}}else n.setState({selected:null,available_move:[]})}}else alert("Choose Computer First Move [Game Type]")},n.state=x,n}return Object(m.a)(t,e),Object(l.a)(t,[{key:"computer_turn",value:function(e,t,n){var o=this,a={boardstate:e,was_capture:t,depth:n},s=[],r=[];S.a.post("/pass",a).then((function(t){for(var n,a=t.data.move_log,i=t.data.movedict,l=a[0],c=0;c<a.length;c++){n=a[c],e=e.map((function(e){return"none eaten"===e?"none":e}));for(var u=i[n],m=0;m<u.length;m++)e[u[m]]="none eaten";s=s.concat([n]),e[l]="none",e[l=n]="two",r=r.concat([e])}o.iterate_move(s,r,[],0)})).catch((function(e){alert(e)}))}},{key:"iterate_move",value:function(e,t,n,o){var a=this,s=e.shift(),r=t.shift();console.log(1e3),console.log(r),console.log(s),n.push(s),0!==e.length?(this.setState({history:this.state.history.concat([{boardState:r}]),selected:s,step_number:this.state.history.length,visited:n}),setTimeout((function(){a.iterate_move(e,t,n,1e3)}),1e3)):this.resetState(r)}},{key:"wait_computer",value:function(){var e=this.getCurrentState(),t=this.state.was_capture,n=this.state.depth;this.computer_turn(e,t,n),this.setState({computer_move:!1,visited:[]})}},{key:"getCurrentState",value:function(){var e=this.state.history;return(e.length>1?(e=e.slice(0,this.state.step_number+1))[e.length-1]:e[0]).boardState}},{key:"AppendHistory",value:function(e){return this.state.history_turn.concat([e])}},{key:"render",value:function(){var e,t=this,n=this.getCurrentState(),o=this.state.selected,s=this.state.available_move,r=this.state.must_choose;if(this.state.turn_number>=4){var i=function(e){for(var t=0,n=0,o=0;o<50;o++)"one"===e[o]?++t:"two"===e[o]&&++n;return 0===t?"Computer WIN":0===n?"You WIN":null}(n);i&&(alert("game over: "+i),this.restart_board())}e=this.state.is_moving?"Computer is moving...":r.length?"Choose: "+d(r[0])+" or "+d(r[1]):o?"Piece selected: "+d(o):"Human to move";var l=function(e){for(var t=[],n=e.length,o=0;o<n;o++)o%2===0?t.push({turn:o/2+1,human:e[o].human,computer:" "}):t[t.length-1].computer=e[o].human;return t}(this.state.history_turn.slice(1)),c="human"===this.state.move_first;return n||this.restart_board(),a.a.createElement("div",{className:"main"},a.a.createElement(g.a,{fluid:!0,id:"container1"},a.a.createElement(y.a,{noGutters:!0},a.a.createElement(E.a,{xs:12,sm:12,md:8},a.a.createElement(R.a,{className:"form_command"},a.a.createElement(R.a.Row,{className:"justify-content-md-center"},a.a.createElement(R.a.Group,{as:E.a,md:"3",xs:"4",controlId:"opponent"},a.a.createElement(R.a.Label,null,"Move First"),a.a.createElement(R.a.Control,{value:"human",as:"select",onChange:this.handle_move_first},a.a.createElement("option",{value:"computer"},"Computer"),a.a.createElement("option",{value:"human"},"Human"))),a.a.createElement(R.a.Group,{as:E.a,md:"3",xs:"4",controlId:"move_first"},a.a.createElement(R.a.Label,null,"Game Type"),a.a.createElement(R.a.Control,{disabled:c,value:this.state.game_type,as:"select",onChange:this.handle_game_type},a.a.createElement("option",{value:"vakyloha"},"Vaky loha"),a.a.createElement("option",{value:"kobana"},"Kobana"),a.a.createElement("option",{value:"fohy"},"Fohy"),a.a.createElement("option",{value:"havia"},"Havia"),a.a.createElement("option",{value:"havanana"},"Havanana"))),a.a.createElement(R.a.Group,{as:E.a,md:"3",xs:"4",controlId:"depth"},a.a.createElement(R.a.Label,null,"Depth"),a.a.createElement(R.a.Control,{value:this.state.depth,as:"select",onChange:this.handle_depth},a.a.createElement("option",null,"1"),a.a.createElement("option",null,"2"),a.a.createElement("option",null,"3"),a.a.createElement("option",null,"4"),a.a.createElement("option",null,"5"))))))),a.a.createElement(y.a,{noGutters:!0},a.a.createElement("div",{className:"windowa"},a.a.createElement(y.a,{noGutters:!0},a.a.createElement(E.a,{xs:12,sm:12,md:8,className:"game_windows row-eq-height"},a.a.createElement("div",{className:"aspect_ratiodiv"},a.a.createElement(g.a,{fluid:!0,className:"BoardCont"},a.a.createElement(y.a,{noGutters:!0,className:"crosscont"},a.a.createElement("div",{className:"aspect_ratiodiv1"},a.a.createElement(j,{boardstate:n,selected:o,available_move:s,onClick:function(e){return t.onClick(e)}}))),a.a.createElement(y.a,{noGutters:!0,className:"command_button"},a.a.createElement(E.a,{style:{textAlign:"center"}},a.a.createElement("button",{className:"game_button",onClick:function(){return t.restart_board()}},"Restart")),a.a.createElement(E.a,{style:{textAlign:"center"}},a.a.createElement("button",{className:"game_button",onClick:function(){return t.pass_game()}},"Pass")),a.a.createElement(E.a,{style:{textAlign:"center"}},a.a.createElement("button",{className:"game_button",onClick:function(){return t.undo_move()}},"Undo")))))),a.a.createElement(E.a,{xs:12,sm:12,md:4,className:"status_window row-eq-height"},a.a.createElement(N,{status:e,move_string:l})))))))}}]),t}(a.a.Component)),k=function(e){var t=e.id,n=d(t),o=e.selected,s=e.available,r="player-"+e.stoneClasses+" "+n;return t===o&&(r+="  selected"),s.indexOf(t)>-1&&(r+="  available"),a.a.createElement("div",{className:r,id:t,onClick:e.onClick})},N=function(e){function t(){return Object(i.a)(this,t),Object(c.a)(this,Object(u.a)(t).apply(this,arguments))}return Object(m.a)(t,e),Object(l.a)(t,[{key:"renderTableData",value:function(){return this.props.move_string.map((function(e,t){var n=e.turn,o=e.human,s=e.computer;return a.a.createElement("tr",{key:n},a.a.createElement("td",{style:{textAlign:"center"}},n),a.a.createElement("td",null,o),a.a.createElement("td",null,s))}))}},{key:"render",value:function(){var e=this.props.status;return a.a.createElement("div",{className:"box_status"},a.a.createElement(g.a,{fluid:!0,className:"status_show"},a.a.createElement("h3",null,"Game Status"),a.a.createElement(y.a,{noGutters:!0,className:"game_status"},a.a.createElement(E.a,{className:"col-centered",id:"log_status"},a.a.createElement("div",{className:"center-me",id:"statusbox"}," ",e))),a.a.createElement("h3",null,"Moves"),a.a.createElement(y.a,{noGutters:!0,className:"moves_log"},a.a.createElement(E.a,{className:"moves_tables"},a.a.createElement("div",{id:"statusall"},a.a.createElement("table",{id:"moves",style:{width:"100%"}},a.a.createElement("thead",null,a.a.createElement("tr",{style:{borderBottom:"1px dashed",borderCollapse:"collapse"}},a.a.createElement("th",{width:"20%",style:{textAlign:"center"}},"ID"),a.a.createElement("th",{width:"40%"},"Human"),a.a.createElement("th",{width:"40%"},"Computer"))),a.a.createElement("tbody",null,this.renderTableData())))))))}}]),t}(a.a.Component),j=function(e){function t(){var e,n;Object(i.a)(this,t);for(var o=arguments.length,s=new Array(o),r=0;r<o;r++)s[r]=arguments[r];return(n=Object(c.a)(this,(e=Object(u.a)(t)).call.apply(e,[this].concat(s)))).RenderStones=function(e){var t=n.props.boardstate[e],o=n.props.selected,s=n.props.available_move;return a.a.createElement(k,{stoneClasses:t,id:e,selected:o,available:s,onClick:function(){return n.props.onClick(e)}})},n}return Object(m.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){return a.a.createElement("div",{className:"rowcross"},a.a.createElement("div",{className:"crossed"},this.RenderStones(49),this.RenderStones(48),this.RenderStones(39),this.RenderStones(38)),a.a.createElement("div",{className:"crossed"},this.RenderStones(47),this.RenderStones(46),this.RenderStones(37),this.RenderStones(36)),a.a.createElement("div",{className:"crossed"},this.RenderStones(45),this.RenderStones(44),this.RenderStones(35),this.RenderStones(34)),a.a.createElement("div",{className:"crossed_left"},this.RenderStones(43),this.RenderStones(42),this.RenderStones(41),this.RenderStones(33),this.RenderStones(32),this.RenderStones(31)),a.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(29),this.RenderStones(28),this.RenderStones(19),this.RenderStones(18),this.RenderStones(9),this.RenderStones(8)),a.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(27),this.RenderStones(26),this.RenderStones(17),this.RenderStones(16),this.RenderStones(7),this.RenderStones(6)),a.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(25),this.RenderStones(24),this.RenderStones(15),this.RenderStones(14),this.RenderStones(5),this.RenderStones(4)),a.a.createElement("div",{className:"crossed_bottom_left"},this.RenderStones(23),this.RenderStones(22),this.RenderStones(21),this.RenderStones(13),this.RenderStones(12),this.RenderStones(11),this.RenderStones(3),this.RenderStones(2),this.RenderStones(1)))}}]),t}(a.a.Component),x={history:[{boardState:h(173538815,562399469895680)}],selected:null,step_number:0,has_moved:null,available_move:[],visited:[],must_choose:[],computer_move:!1,is_moving:!1,was_capture:!1,status:null,depth:3,game_type:null,move_first:"human",history_turn:[{boardState:h(173538815,562399469895680),turn_id:0,human:"",computer:""}],turn_number:0},O=C;Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));n(268);r.a.render(a.a.createElement(O,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[103,1,2]]]);
//# sourceMappingURL=main.00a2b3f0.chunk.js.map