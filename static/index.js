var row = 0;
var favorites = [];
var ts_lines = "";

window.onload = function() {
  for (x in ts_lines) {
    var row = ts_lines[x]
    addRow(row["fav"],row["note"],row["times"]);
  }
  if (ts_lines.length == 0){
    addBlankRow()
  }
  for (d of ["mon", "tue", "wed", "thu", "fri"]) {
    updateTotals(d);
  }
}

function init(ts, faves) {
  favorites = faves;
  ts_lines = ts;
}

function addBlankRow() {
  addRow(favorites[0],"",[0,0,0,0,0]);
}

function addRow(fav, note, times) {
  const div = document.createElement('div');
  div.className = 'row';
  var inner = `<select name="fave${row}" id="fave${row}">`;

  for (x of favorites){
    inner = inner + `<option value="${x}">${x}</option>`;
  }

  inner = inner + `</select>
  <input name="description${row}" class="description" value="${note}">
  <input name="mon${row}" type="number" min="0" class="hours" step="any" value="${times[0]}" oninput="updateTotals('mon')">
  <input name="tue${row}" type="number" min="0" class="hours" step="any" value="${times[1]}" oninput="updateTotals('tue')">
  <input name="wed${row}" type="number" min="0" class="hours" step="any" value="${times[2]}" oninput="updateTotals('wed')">
  <input name="thu${row}" type="number" min="0" class="hours" step="any" value="${times[3]}" oninput="updateTotals('thu')">
  <input name="fri${row}" type="number" min="0" class="hours" step="any" value="${times[4]}" oninput="updateTotals('fri')">
  <br>
  `;
  div.innerHTML = inner;
  document.getElementById('content').appendChild(div);
  var select = document.getElementById("fave"+row);
  select.value = fav;
  row = row+1
}

function updateTotals(day) {
  var dayt = 0;
  for (i = 0; i < row; i++) {
    var val = document.getElementsByName(day+i.toString())[0].value;
    dayt += parseFloat(val);
  }
  var t = document.getElementById("t"+day);
  t.innerHTML = dayt;
  var total = 0;
  for (d of ["tmon", "ttue", "twed", "tthu", "tfri"]){
    total = total + parseFloat(document.getElementById(d).innerHTML);
  }
  var f = document.getElementById("total");
  f.innerHTML = "Current Time Total: "+ total.toString();
}
