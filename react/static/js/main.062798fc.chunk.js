(this["webpackJsonpmy-app"]=this["webpackJsonpmy-app"]||[]).push([[0],{27:function(e,t,a){e.exports=a(56)},32:function(e,t,a){},33:function(e,t,a){},56:function(e,t,a){"use strict";a.r(t);var n=a(0),s=a.n(n),o=a(23),r=a.n(o),i=(a(32),a(7)),l=a(8),c=a(10),u=a(9),m=a(6),d=a(11);a(33);function h(e,t){for(var a=Array(50).fill("none"),n=e.toString(2).padStart(64,"0"),s=t.toString(2).padStart(64,"0"),o=n.length,r=s.length,i=0;i<50;i++)"1"===n.charAt(o-i)?a[i]="one":"1"===s.charAt(r-i)?a[i]="two":a[i]="none";return a}function v(e){return{0:"e",1:"d",2:"c",3:"b",4:"a"}[~~(e/10)]+(10-e%10)}function p(e){for(var t=0;t<e.length;t++)if(0===t)var a=v(e[t]);else a=a+"-"+v(e[t]);return a}function _(e,t,a,n){var s,o,r=[];s=t%2!==~~(t/10)%2?[-11,-10,-9,-1,1,9,10,11]:[-10,-1,1,10];for(var i=0;i<s.length;i++){var l=t+s[i];if(l%10!==0&&(("none"===e[l]||"none eaten"===e[l])&&!a.includes(l)))if(n){var c=a.length;if(c>1){var u=a[c-2];o=a[c-1]-u}else o=0,0;f(e,t,s[i])&&s[i]!==o&&r.push(l)}else r.push(t+s[i])}return r}function f(e,t,a){return"two"===e[t+2*a]||"two"===e[t-a]}function S(e,t){return!!t||function(e){for(var t=e.reduce((function(e,t,a){return"one"===t?e.concat(a):e}),[]),a=[],n=0;n<t.length;n++)if(_(e,t[n],a,!0).length>=1)return!0;return!1}(e)}var b=a(24),g=a.n(b),E=a(58),y=a(59),R=a(26),w=a(60),C=function(e){function t(e){var a;return Object(i.a)(this,t),(a=Object(c.a)(this,Object(u.a)(t).call(this,e))).componentDidUpdate=function(){a.state.computer_move&&(a.setState({is_moving:!0}),a.wait_computer(),a.setState({computer_move:!1,is_moving:!1}),console.log(Object(m.a)(a)))},a.restart_board=function(){a.setState({history:[{boardState:h(173538815,562399469895680)}],selected:null,step_number:0,has_moved:null,available_move:[],must_choose:[],status:"Human to move"})},a.undo_move=function(){var e=parseInt(a.state.step_number,10)-1;if(!(e<0)){var t=a.state.history.slice(0,e+1);a.setState({history:t,selected:null,available_move:[],visited:[],must_choose:[],step_number:e,new_pos:null})}},a.resetState=function(e){var t=p(a.state.visited),n=a.state.turn_number;if(a.state.is_moving)(o=a.state.history_turn)[n].computer=t;else var s={boardState:e,turn_id:n+=1,human:t,computer:""},o=a.AppendHistory(s);a.setState({history:a.state.history.concat([{boardState:e}]),selected:null,computer_move:!1,available_move:[],visited:[],has_moved:!1,must_choose:[],step_number:a.state.history.length,status:"Computer is moving",history_turn:o,turn_number:n})},a.pass_game=function(){if(a.state.has_moved){var e=p(a.state.visited),t=a.state.turn_number+1,n={boardState:a.getCurrentState(),turn_id:t,human:e,computer:""};a.setState({was_capture:!0,computer_move:!0,selected:null,status:"Computer is moving",available_move:[],visited:[],has_moved:!1,must_choose:[],history_turn:a.AppendHistory(n),turn_number:t})}},a.handle_opp_change=function(e){a.setState({opponent:e.target.value})},a.handle_movefirst=function(e){a.setState({move_first:e.target.value})},a.handle_depth=function(e){a.setState({depth:e.target.value})},a.onClick=function(e){if(!a.state.computer_move){var t,n,s,o,r,i,l=a.state.must_choose,c=a.state.selected,u=a.getCurrentState(),m=a.state.visited,d=a.state.has_moved;if(l.length>1){if(!l.includes(e))return void alert("you must choose");var h=a.state.new_pos;if((s=function(e,t,a){var n=a-t;n%2===0&&10!==Math.abs(n)&&(n/=2);for(var s=a;"two"===e[s];)e[s]="none eaten",s+=n;return e}(u,c,e))[c]="none",s[h]="one",d||m.push(c),m.push(h),n=_(u,e,m,o=S(s,!0)),!(o&&n>0))return a.resetState(s),void a.setState({was_capture:!0,computer_move:!0,visited:[]});a.setState({history:a.state.history.concat([{boardState:s,currentPlayer:!0}]),must_choose:[],selected:h,visited:m,has_moved:!0})}o=S(u,a.state.has_moved);var v=a.state.available_move;if(c!==e||d){if(c&&"one"===u[e]&&!d){if(!((n=_(u,e,m,o)).length>0))return;a.setState({selected:e,available_move:n})}if(!c&&!a.state.computer_move){if("one"!==u[e])return;if(!((n=_(u,e,m,o)).length>0))return;a.setState({selected:e,available_move:n})}if(v.includes(e)){if(r=c-(t=e-c),"two"===u[i=c+2*t]&&"two"===u[r])return a.setState({must_choose:[i,r],new_pos:e}),void alert("must choose");if(s=function(e,t,a,n){var s,o;for("two"===(e=e.map((function(e){return"none eaten"===e?"none":e})))[t+2*n]?o=a+(s=n):"two"===e[t-n]&&(o=a+2*(s=-n)),e[t]="none",e[a]="one";"two"===e[o];)e[o]="none eaten",o+=s;return e}(u,c,e,t),d||m.push(c),m.push(e),!o)return a.resetState(s),void a.setState({was_capture:!1,computer_move:!0,visited:[]});if(!((n=_(s,e,m,o)).length>=1))return a.resetState(s),void a.setState({was_capture:!0,computer_move:!0,visited:[]});a.setState({history:a.state.history.concat([{boardState:s,currentPlayer:!0}]),selected:e,available_move:n,has_moved:!0,visited:m,must_choose:[],step_number:a.state.history.length})}}else a.setState({selected:null,available_move:[]})}},a.state={width:100,height:100,history:[{boardState:h(173538815,562399469895680)}],selected:null,step_number:0,has_moved:null,available_move:[],visited:[],must_choose:[],computer_move:!1,move_log:[],move_logback:[],states:[],is_moving:!1,was_capture:!1,status:null,opponent:"computer",move_first:"human",depth:3,move_string:[],history_turn:[{boardState:[],turn_id:0,human:"",computer:""}],turn_number:0},a}return Object(d.a)(t,e),Object(l.a)(t,[{key:"computer_turn",value:function(e,t,a){var n=this,s={boardstate:e,was_capture:t,depth:a},o=[],r=[];g.a.post("/pass",s).then((function(t){for(var a,s=t.data.move_log,i=t.data.movedict,l=s[0],c=0;c<s.length;c++){e[l]="none",a=s[c],e[a]="two",e=e.map((function(e){return"none eaten"===e?"none":e}));for(var u=i[a],m=0;m<u.length;m++)e[u[m]]="none eaten";l=a,o=o.concat([l]),r=r.concat([e])}n.setState({move_log:o,move_logback:o,states:r}),setTimeout((function(){n.iterate_move(o,r)}),1e3)})).catch((function(e){alert(e)}))}},{key:"iterate_move",value:function(e,t){var a=this;setTimeout((function(){var n=e.shift(),s=t.shift(),o=a.state.visited;if(0===e.length)return o.push(n),a.resetState(s),void a.setState({computer_move:!1,visited:[]});o.push(n),a.setState({history:a.state.history.concat([{boardState:s}]),selected:n,step_number:a.state.history.length-1,visited:o}),a.iterate_move(e,t)}),1e3)}},{key:"wait_computer",value:function(){var e=this.getCurrentState(),t=this.state.was_capture,a=this.state.depth;this.computer_turn(e,t,a)}},{key:"AImoves",value:function(){var e=this.state.move_log,t=this.state.states;this.iterate_move(e,t)}},{key:"getCurrentState",value:function(){var e=this.state.history;return(e.length>1?(e=e.slice(0,this.state.step_number+1))[e.length-1]:e[0]).boardState}},{key:"AppendHistory",value:function(e){return this.state.history_turn.concat([e])}},{key:"render",value:function(){var e,t=this,a=this.getCurrentState(),n=this.state.selected,o=this.state.available_move,r=function(e){for(var t=0,a=0,n=0;n<50;n++)"one"===e[n]?++t:"two"===e[n]&&++a;return 0===t?"Computer WIN":0===a?"You WIN":null}(a),i=this.state.must_choose;r&&(alert("game over: "+r),this.restart_board()),e=this.state.is_moving?"Computer is moving...":i.length?"Choose: "+v(i[0])+" or "+v(i[1]):n?"Piece selected: "+v(n):"Human to move";var l=this.state.history_turn.slice(1);console.log(l);var c=function(e){for(var t=[],a=e.length,n=0;n<a;n+=2)n%2===0?t.push([{turn:n/2+1,human:e[n].human,computer:" "}]):t[n/2].computer=e[n].human;return t}(l);return console.log(c),s.a.createElement("div",{className:"main"},s.a.createElement(E.a,{fluid:!0,id:"container1"},s.a.createElement(y.a,{noGutters:!0},s.a.createElement(R.a,{xs:12,sm:12,md:8},s.a.createElement(w.a,{className:"form_command"},s.a.createElement(w.a.Row,{className:"justify-content-md-center"},s.a.createElement(w.a.Group,{as:R.a,md:"3",xs:"4",controlId:"opponent"},s.a.createElement(w.a.Label,null,"Opponent"),s.a.createElement(w.a.Control,{value:this.state.opponent,as:"select",onChange:this.handle_opp_change},s.a.createElement("option",{value:"computer"},"Computer"),s.a.createElement("option",{value:"human"},"Human"))),s.a.createElement(w.a.Group,{as:R.a,md:"3",xs:"4",controlId:"move_first"},s.a.createElement(w.a.Label,null,"Move First"),s.a.createElement(w.a.Control,{value:this.state.movefirst,as:"select",onChange:this.handle_movefirst},s.a.createElement("option",{value:"computer"},"Computer"),s.a.createElement("option",{value:"human"},"Human"))),s.a.createElement(w.a.Group,{as:R.a,md:"3",xs:"4",controlId:"depth"},s.a.createElement(w.a.Label,null,"Depth"),s.a.createElement(w.a.Control,{value:this.state.depth,as:"select",onChange:this.handle_depth},s.a.createElement("option",null,"1"),s.a.createElement("option",null,"2"),s.a.createElement("option",null,"3"),s.a.createElement("option",null,"4"),s.a.createElement("option",null,"5"))))))),s.a.createElement(y.a,{noGutters:!0,className:"windowa"},s.a.createElement(R.a,{xs:12,sm:12,md:8,className:"game_windows row-eq-height"},s.a.createElement("div",{className:"aspect_ratiodiv"},s.a.createElement(E.a,{fluid:!0,className:"BoardCont"},s.a.createElement(y.a,{noGutters:!0,className:"crosscont"},s.a.createElement("div",{className:"aspect_ratiodiv1"},s.a.createElement(O,{boardstate:a,selected:n,available_move:o,onClick:function(e){return t.onClick(e)}}))),s.a.createElement(y.a,{noGutters:!0,className:"command_button"},s.a.createElement(R.a,{style:{textAlign:"center"}},s.a.createElement("button",{className:"game_button",onClick:function(){return t.restart_board()}},"Restart")),s.a.createElement(R.a,{style:{textAlign:"center"}},s.a.createElement("button",{className:"game_button",onClick:function(){return t.pass_game()}},"Pass")),s.a.createElement(R.a,{style:{textAlign:"center"}},s.a.createElement("button",{className:"game_button",onClick:function(){return t.undo_move()}},"Undo")))))),s.a.createElement(R.a,{xs:12,sm:12,md:4,className:"status_window row-eq-height"},s.a.createElement(k,{status:e,move_string:c})))))}}]),t}(s.a.Component),N=function(e){var t=e.id,a=v(t),n=e.selected,o=e.available,r="player-"+e.stoneClasses+" "+a;return t===n&&(r+="  selected"),o.indexOf(t)>-1&&(r+="  available"),s.a.createElement("div",{className:r,id:t,onClick:e.onClick})},k=function(e){function t(){return Object(i.a)(this,t),Object(c.a)(this,Object(u.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(l.a)(t,[{key:"renderTableData",value:function(){var e=this.props.move_string;return console.log(e),e.map((function(e,t){var a=e.turn_id,n=e.human,o=e.computer;return s.a.createElement("tr",{key:a},s.a.createElement("td",null,a),s.a.createElement("td",null,n),s.a.createElement("td",null,o))}))}},{key:"render",value:function(){var e=this.props.status;return s.a.createElement("div",{className:"box_status"},s.a.createElement(E.a,{fluid:!0,className:"status_show"},s.a.createElement("h3",null,"Game Status"),s.a.createElement(y.a,{noGutters:!0,className:"game_status"},s.a.createElement(R.a,{className:"col-centered",id:"log_status"},s.a.createElement("div",{className:"center-me",id:"statusbox"}," ",e))),s.a.createElement("h3",null,"Moves"),s.a.createElement(y.a,{noGutters:!0,className:"moves_log"},s.a.createElement(R.a,{className:"moves_tables"},s.a.createElement("div",{id:"statusall"},s.a.createElement("table",{id:"moves"},s.a.createElement("tbody",null,this.renderTableData())))))))}}]),t}(s.a.Component),O=function(e){function t(){var e,a;Object(i.a)(this,t);for(var n=arguments.length,o=new Array(n),r=0;r<n;r++)o[r]=arguments[r];return(a=Object(c.a)(this,(e=Object(u.a)(t)).call.apply(e,[this].concat(o)))).RenderStones=function(e){var t=a.props.boardstate[e],n=a.props.selected,o=a.props.available_move;return s.a.createElement(N,{stoneClasses:t,id:e,selected:n,available:o,onClick:function(){return a.props.onClick(e)}})},a}return Object(d.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){return s.a.createElement("div",{className:"rowcross"},s.a.createElement("div",{className:"crossed"},this.RenderStones(49),this.RenderStones(48),this.RenderStones(39),this.RenderStones(38)),s.a.createElement("div",{className:"crossed"},this.RenderStones(47),this.RenderStones(46),this.RenderStones(37),this.RenderStones(36)),s.a.createElement("div",{className:"crossed"},this.RenderStones(45),this.RenderStones(44),this.RenderStones(35),this.RenderStones(34)),s.a.createElement("div",{className:"crossed_left"},this.RenderStones(43),this.RenderStones(42),this.RenderStones(41),this.RenderStones(33),this.RenderStones(32),this.RenderStones(31)),s.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(29),this.RenderStones(28),this.RenderStones(19),this.RenderStones(18),this.RenderStones(9),this.RenderStones(8)),s.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(27),this.RenderStones(26),this.RenderStones(17),this.RenderStones(16),this.RenderStones(7),this.RenderStones(6)),s.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(25),this.RenderStones(24),this.RenderStones(15),this.RenderStones(14),this.RenderStones(5),this.RenderStones(4)),s.a.createElement("div",{className:"crossed_bottom_left"},this.RenderStones(23),this.RenderStones(22),this.RenderStones(21),this.RenderStones(13),this.RenderStones(12),this.RenderStones(11),this.RenderStones(3),this.RenderStones(2),this.RenderStones(1)))}}]),t}(s.a.Component),j=C;Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));a(55);r.a.render(s.a.createElement(j,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[27,1,2]]]);
//# sourceMappingURL=main.062798fc.chunk.js.map