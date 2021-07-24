function parse(d) {
  var f = d.split('%'),
  c = 0,
  b = 0,
  g,
  a;
  while (c < f.length) {
    g = required[b++];
    a = {
      landscape: zero(f[c++], 10),
      mapclass: 0,
      text: '',
      cached: false
    };
    a.mapclass = a.landscape >= 50 && a.landscape <= 59 ? 1 : a.landscape >= 30 && a.landscape <= 39 ? 3 : a.landscape >= 20 && a.landscape <= 29 ? 10 : a.landscape == 90 ? 5 : a.landscape == 91 ? 8 : 0;
    switch (a.mapclass) {
      case 0:
      case 10:
        a.text = '<p>' + _emptyGround + '</p>';
        switch (zero(f[c++], 0)) {
          case 0:
            a.text += fields(3, 3, 4, 0);
            break;
          case 1:
            a.text += fields(4, 2, 4, 0);
            break;
          case 2:
            a.text += fields(2, 4, 4, 0);
            break;
          case 3:
            a.text += fields(2, 2, 6, 0);
            break;
          case 4:
            a.text += fields(4, 4, 2, 0);
            break;
          case 5:
            a.text += fields(1, 1, 8, 0);
            break;
          case 7:
            a.text += fields(0, 0, 2, 8);
            break;
          case 8:
            a.text += fields(2, 2, 4, 2);
            break;
          default:
            alert('unexpected fields config ' + g);
            return
        }
        if (a.mapclass == 10) {
          a.text += '<p><b>' + _debrisField + '</b></p>'
        }
        break;
      case 8:
        a.text = '<p>' + _disabledGround + '</p>';
        break;
      case 1:
        a.text = '<p>' + _city + ' <b>' + f[c++] + '</b></p><p>' + _points + ' <b>' + f[c++] + '</b></p><p>' + _player + ' <b>' + f[c++] + '</b></p>' + (f[c].length == 0 ? '' : '<p>' + _alliance + ' <b>' + f[c] + '</b></p>');
        ++c;
        break;
      case 3:
        a.text = '<p>' + f[c++] + '</p><p>' + _npc + '</p>';
        break;
      case 5:
        a.text = '<p>' + f[c++] + '</p>' + (f[c].length == 0 ? '' : '<p>' + _alliance + ' <b>' + f[c] + '</b></p>');
        ++c;
        break
    }
    console.log(a.text)
  }
}