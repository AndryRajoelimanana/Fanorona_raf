(this["webpackJsonpmy-app"]=this["webpackJsonpmy-app"]||[]).push([[0],{27:function(e,t,a){e.exports=a(56)},32:function(e,t,a){},33:function(e,t,a){},56:function(e,t,a){"use strict";a.r(t);var n=a(0),s=a.n(n),o=a(23),r=a.n(o),i=(a(32),a(7)),l=a(8),c=a(10),m=a(9),u=a(6),d=a(11);a(33);function h(e,t){for(var a=Array(50).fill("none"),n=e.toString(2).padStart(64,"0"),s=t.toString(2).padStart(64,"0"),o=n.length,r=s.length,i=0;i<50;i++)"1"===n.charAt(o-i)?a[i]="one":"1"===s.charAt(r-i)?a[i]="two":a[i]="none";return a}function v(e){return{0:"e",1:"d",2:"c",3:"b",4:"a"}[~~(e/10)]+(10-e%10)}function p(e,t,a,n){var s,o,r=[];s=t%2!==~~(t/10)%2?[-11,-10,-9,-1,1,9,10,11]:[-10,-1,1,10];for(var i=0;i<s.length;i++){var l=t+s[i];if(l%10!==0&&(("none"===e[l]||"none eaten"===e[l])&&!a.includes(l)))if(n){var c=a.length;if(c>1){var m=a[c-2];o=a[c-1]-m}else o=0,0;_(e,t,s[i])&&s[i]!==o&&r.push(l)}else r.push(t+s[i])}return r}function _(e,t,a){return"two"===e[t+2*a]||"two"===e[t-a]}function f(e,t){return!!t||function(e){for(var t=e.reduce((function(e,t,a){return"one"===t?e.concat(a):e}),[]),a=[],n=0;n<t.length;n++)if(p(e,t[n],a,!0).length>=1)return!0;return!1}(e)}var S=a(24),b=a.n(S),g=a(58),E=a(59),R=a(26),w=a(60),y=function(e){function t(e){var a;return Object(i.a)(this,t),(a=Object(c.a)(this,Object(m.a)(t).call(this,e))).componentDidUpdate=function(){a.state.computer_move&&(a.setState({is_moving:!0}),a.wait_computer())},a.restart_board=function(){a.setState({history:[{boardState:h(173538815,562399469895680)}],selected:null,step_number:0,has_moved:null,available_move:[],visited:[],must_choose:[],status:"Human to move"})},a.undo_move=function(){var e=parseInt(a.state.step_number,10)-1;if(!(e<0)){var t=a.state.history.slice(0,e+1);a.setState({history:t,selected:null,available_move:[],visited:[],must_choose:[],step_number:e,new_pos:null})}},a.resetState=function(e){a.setState({history:a.state.history.concat([{boardState:e}]),selected:null,computer_move:!1,available_move:[],visited:[],has_moved:!1,must_choose:[],step_number:a.state.history.length,status:"Computer is moving"})},a.pass_game=function(){a.setState({was_capture:!0,computer_move:!0,status:"Human to move"})},a.handle_opp_change=function(e){a.setState({opponent:e.target.value}),console.log(Object(u.a)(a))},a.handle_movefirst=function(e){a.setState({move_first:e.target.value}),console.log(Object(u.a)(a))},a.handle_depth=function(e){a.setState({depth:e.target.value}),console.log(Object(u.a)(a))},a.onClick=function(e){if(!a.state.computer_move){var t,n,s,o,r,i,l=a.state.must_choose,c=a.state.selected,m=a.getCurrentState(),u=a.state.visited,d=a.state.has_moved;if(l.length>1){if(!l.includes(e))return void alert("you must choose");var h=a.state.new_pos;if((s=function(e,t,a){for(var n=a-t,s=a;"two"===e[s];)e[s]="none eaten",s+=n;return e}(m,c,e))[c]="none",s[h]="one",d||u.push(c),u.push(h),o=f(s,!0),console.log(u),n=p(m,e,u,o),!(o&&n>0))return a.resetState(s),void a.setState({was_capture:!0,computer_move:!0});a.setState({history:a.state.history.concat([{boardState:s,currentPlayer:!0}]),must_choose:[],selected:h,visited:u,has_moved:!0})}o=f(m,a.state.has_moved);var v=a.state.available_move;if(c!==e||d){if(c&&"one"===m[e]&&!d){if(!((n=p(m,e,u,o)).length>0))return;a.setState({selected:e,available_move:n})}if(!c&&!a.state.computer_move){if("one"!==m[e])return;if(!((n=p(m,e,u,o)).length>0))return;a.setState({selected:e,available_move:n})}if(v.includes(e)){if(r=c-(t=e-c),"two"===m[i=c+2*t]&&"two"===m[r])return a.setState({must_choose:[i,r],new_pos:e}),void alert("must choose");if(s=function(e,t,a,n){var s,o;for("two"===(e=e.map((function(e){return"none eaten"===e?"none":e})))[t+2*n]?o=a+(s=n):"two"===e[t-n]&&(o=a+2*(s=-n)),e[t]="none",e[a]="one";"two"===e[o];)e[o]="none eaten",o+=s;return e}(m,c,e,t),d||u.push(c),u.push(e),!o)return a.resetState(s),void a.setState({was_capture:!1,computer_move:!0});if(!((n=p(s,e,u,o)).length>=1))return a.resetState(s),void a.setState({was_capture:!0,computer_move:!0});a.setState({history:a.state.history.concat([{boardState:s,currentPlayer:!0}]),selected:e,available_move:n,has_moved:!0,visited:u,must_choose:[],step_number:a.state.history.length})}}else a.setState({selected:null,available_move:[]})}},a.state={width:100,height:100,history:[{boardState:h(173538815,562399469895680)}],selected:null,step_number:0,has_moved:null,available_move:[],visited:[],must_choose:[],computer_move:!1,move_log:[],states:[],is_moving:!1,was_capture:!1,status:null,opponent:"computer",move_first:"human",depth:3},a}return Object(d.a)(t,e),Object(l.a)(t,[{key:"computer_turn",value:function(e,t,a){var n=this,s={boardstate:e,was_capture:t,depth:a},o=[],r=[];b.a.post("/pass",s).then((function(t){for(var a,s=t.data.move_log,i=t.data.movedict,l=s[0],c=0;c<s.length;c++){e[l]="none",a=s[c],e[a]="two",e=e.map((function(e){return"none eaten"===e?"none":e}));for(var m=i[a],u=0;u<m.length;u++)e[m[u]]="none eaten";l=a,o=o.concat([l]),r=r.concat([e])}n.setState({move_log:o,states:r}),setTimeout((function(){n.iterate_move(o,r)}),1e3)})).catch((function(e){alert(e)}))}},{key:"iterate_move",value:function(e,t){var a=this;setTimeout((function(){var n=e.shift(),s=t.shift();if(0===e.length)return a.resetState(s),void a.setState({computer_move:!1});a.setState({history:a.state.history.concat([{boardState:s}]),selected:n,step_number:a.state.history.length-1}),a.iterate_move(e,t)}),1e3)}},{key:"wait_computer",value:function(){var e=this.getCurrentState(),t=this.state.was_capture,a=this.state.depth;this.computer_turn(e,t,a),this.setState({computer_move:!1,is_moving:!1})}},{key:"AImoves",value:function(){var e=this.state.move_log,t=this.state.states;this.iterate_move(e,t)}},{key:"getCurrentState",value:function(){var e=this.state.history;return(e.length>1?(e=e.slice(0,this.state.step_number+1))[e.length-1]:e[0]).boardState}},{key:"render",value:function(){var e,t=this,a=this.getCurrentState(),n=this.state.selected,o=this.state.available_move,r=function(e){for(var t=0,a=0,n=0;n<50;n++)"one"===e[n]?++t:"two"===e[n]&&++a;return 0===t?"Computer WIN":0===a?"You WIN":null}(a),i=this.state.must_choose;return r&&(alert("game over: "+r),this.restart_board()),e=this.state.is_moving?"Computer is moving...":i.length?"Choose: "+v(i[0])+" or "+v(i[1]):n?"Piece selected: "+v(n):"Human to move",s.a.createElement("div",{className:"main"},s.a.createElement(g.a,{fluid:!0,id:"container1"},s.a.createElement(E.a,{noGutters:!0},s.a.createElement(R.a,{xs:12,sm:12,md:8},s.a.createElement(w.a,{className:"form_command"},s.a.createElement(w.a.Row,{className:"justify-content-md-center"},s.a.createElement(w.a.Group,{as:R.a,md:"3",xs:"4",controlId:"opponent"},s.a.createElement(w.a.Label,null,"Opponent"),s.a.createElement(w.a.Control,{value:this.state.opponent,as:"select",onChange:this.handle_opp_change},s.a.createElement("option",{value:"computer"},"Computer"),s.a.createElement("option",{value:"human"},"Human"))),s.a.createElement(w.a.Group,{as:R.a,md:"3",xs:"4",controlId:"move_first"},s.a.createElement(w.a.Label,null,"Move First"),s.a.createElement(w.a.Control,{value:this.state.movefirst,as:"select",onChange:this.handle_movefirst},s.a.createElement("option",{value:"computer"},"Computer"),s.a.createElement("option",{value:"human"},"Human"))),s.a.createElement(w.a.Group,{as:R.a,md:"3",xs:"4",controlId:"depth"},s.a.createElement(w.a.Label,null,"Depth"),s.a.createElement(w.a.Control,{value:this.state.depth,as:"select",onChange:this.handle_depth},s.a.createElement("option",null,"1"),s.a.createElement("option",null,"2"),s.a.createElement("option",null,"3"),s.a.createElement("option",null,"4"),s.a.createElement("option",null,"5"))))))),s.a.createElement(E.a,{noGutters:!0,className:"windowa"},s.a.createElement(R.a,{xs:12,sm:12,md:8,className:"game_windows row-eq-height"},s.a.createElement("div",{className:"aspect_ratiodiv"},s.a.createElement(g.a,{fluid:!0,className:"BoardCont"},s.a.createElement(E.a,{noGutters:!0,className:"crosscont"},s.a.createElement("div",{className:"aspect_ratiodiv1"},s.a.createElement(k,{boardstate:a,selected:n,available_move:o,onClick:function(e){return t.onClick(e)}}))),s.a.createElement(E.a,{noGutters:!0,className:"command_button"},s.a.createElement(R.a,{style:{textAlign:"center"}},s.a.createElement("button",{className:"game_button",onClick:function(){return t.restart_board()}},"Restart")),s.a.createElement(R.a,{style:{textAlign:"center"}},s.a.createElement("button",{className:"game_button",onClick:function(){return t.pass_game()}},"Pass")),s.a.createElement(R.a,{style:{textAlign:"center"}},s.a.createElement("button",{className:"game_button",onClick:function(){return t.undo_move()}},"Undo")))))),s.a.createElement(R.a,{xs:12,sm:12,md:4,className:"status_window row-eq-height"},s.a.createElement(C,{status:e})))))}}]),t}(s.a.Component),N=function(e){var t=e.id,a=v(t),n=e.selected,o=e.available,r="player-"+e.stoneClasses+" "+a;return t===n&&(r+="  selected"),o.indexOf(t)>-1&&(r+="  available"),s.a.createElement("div",{className:r,id:t,onClick:e.onClick})},C=function(e){function t(){return Object(i.a)(this,t),Object(c.a)(this,Object(m.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){var e=this.props.status;return s.a.createElement("div",{className:"box_status"},s.a.createElement(g.a,{fluid:!0,className:"status_show"},s.a.createElement("h3",null,"Game Status"),s.a.createElement(E.a,{noGutters:!0,className:"game_status"},s.a.createElement(R.a,{className:"col-centered",id:"log_status"},s.a.createElement("div",{className:"center-me",id:"statusbox"}," ",e))),s.a.createElement("h3",null,"Moves"),s.a.createElement(E.a,{noGutters:!0,className:"moves_log"},s.a.createElement(R.a,{className:"moves_tables"},s.a.createElement("div",{className:"scrollbar-inner",id:"statusall"})))))}}]),t}(s.a.Component),k=function(e){function t(){var e,a;Object(i.a)(this,t);for(var n=arguments.length,o=new Array(n),r=0;r<n;r++)o[r]=arguments[r];return(a=Object(c.a)(this,(e=Object(m.a)(t)).call.apply(e,[this].concat(o)))).RenderStones=function(e){var t=a.props.boardstate[e],n=a.props.selected,o=a.props.available_move;return s.a.createElement(N,{stoneClasses:t,id:e,selected:n,available:o,onClick:function(){return a.props.onClick(e)}})},a}return Object(d.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){return s.a.createElement("div",{className:"rowcross"},s.a.createElement("div",{className:"crossed"},this.RenderStones(49),this.RenderStones(48),this.RenderStones(39),this.RenderStones(38)),s.a.createElement("div",{className:"crossed"},this.RenderStones(47),this.RenderStones(46),this.RenderStones(37),this.RenderStones(36)),s.a.createElement("div",{className:"crossed"},this.RenderStones(45),this.RenderStones(44),this.RenderStones(35),this.RenderStones(34)),s.a.createElement("div",{className:"crossed_left"},this.RenderStones(43),this.RenderStones(42),this.RenderStones(41),this.RenderStones(33),this.RenderStones(32),this.RenderStones(31)),s.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(29),this.RenderStones(28),this.RenderStones(19),this.RenderStones(18),this.RenderStones(9),this.RenderStones(8)),s.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(27),this.RenderStones(26),this.RenderStones(17),this.RenderStones(16),this.RenderStones(7),this.RenderStones(6)),s.a.createElement("div",{className:"crossed_bottom"},this.RenderStones(25),this.RenderStones(24),this.RenderStones(15),this.RenderStones(14),this.RenderStones(5),this.RenderStones(4)),s.a.createElement("div",{className:"crossed_bottom_left"},this.RenderStones(23),this.RenderStones(22),this.RenderStones(21),this.RenderStones(13),this.RenderStones(12),this.RenderStones(11),this.RenderStones(3),this.RenderStones(2),this.RenderStones(1)))}}]),t}(s.a.Component),O=y;Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));a(55);r.a.render(s.a.createElement(O,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[27,1,2]]]);
//# sourceMappingURL=main.92f89f65.chunk.js.map